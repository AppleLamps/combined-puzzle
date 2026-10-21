"""Reproduce the exploratory FAED tail lead without promoting it to a delimiter."""
import hashlib
import html
import json
import re
from collections import Counter
from pathlib import Path

import numpy as np
from test_faed_variable_tokens import tokenize, match

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'runs/2026-09-13_faed_tail'


def split_profile(x):
    n = len(x)
    counts = np.bincount(x, minlength=9)
    cuts = np.arange(40, n-39)
    cumulative = np.vstack((np.zeros(9, dtype=int), np.eye(9, dtype=int)[x].cumsum(0)))
    left = cumulative[cuts]
    right = counts-left
    def xl(a):
        return a*np.log(np.maximum(a, 1))
    values = 2*(xl(left).sum(1)+xl(right).sum(1)-xl(counts).sum()
                -xl(cuts)-xl(n-cuts)+xl(np.array(n)))
    return cuts, values


def integer_forms(s):
    forms = {'raw_ascii': s.encode(), 'page_decimal_ascii': s.translate(str.maketrans('abcdefghi', '123456789')).encode()}
    for name, base, alphabet in [('page_decimal_integer', 10, 'oabcdefghi'), ('base9_integer', 9, 'abcdefghi')]:
        number = 0
        for ch in s:
            number = base*number+alphabet.index(ch)
        forms[name] = number.to_bytes((number.bit_length()+7)//8, 'big')
    return forms


def source_copies(expected):
    paths = [ROOT/'originals/pages/salphaseion_phase3.html',
             ROOT.parent/'rabbit-gemini/wayback/salphaseion_2023.html',
             ROOT.parent/'read/salphaseion_page.html',
             ROOT.parent/'rabbitv5/newest-telegram-9.9.26/scratch_gsmg/wayback/salphaseion_live.html']
    records = []
    for path in paths:
        if not path.exists():
            records.append(dict(path=str(path), status='missing'))
            continue
        raw = path.read_bytes()
        areas = re.findall(r'<textarea\b[^>]*>(.*?)</textarea>', raw.decode('utf-8'), re.S|re.I)
        compact = [re.sub(r'\s+', '', html.unescape(a)) for a in areas]
        candidates = [s for s in compact if s.startswith('dbbibf')]
        records.append(dict(path=str(path), file_sha256=hashlib.sha256(raw).hexdigest(),
                            candidates=len(candidates), same_complete_wrapper=expected in candidates,
                            same_faed=[s[195:765] == expected[195:765] for s in candidates],
                            archive_marker=re.findall(r'__wm\.wombat\([^\n]+', raw.decode('utf-8'))[:1]))
    return records


def main():
    OUT.mkdir(exist_ok=True)
    s = (ROOT/'data/FAED_570.txt').read_text().strip()
    d = (ROOT/'data/DBBI_91.txt').read_text().strip()
    wrapper = (ROOT/'data/salphaseion_compact_1075.txt').read_text().strip()
    assert wrapper[195:765] == s
    tokens, spans = tokenize(s, 'bg')
    dtokens, _ = tokenize(d, 'bg')
    x = np.array([ord(c)-97 for c in s])
    cuts, values = split_profile(x)
    maximum = float(values.max())
    best = int(cuts[values.argmax()])
    assert best == 523 and spans[-40] == [522, 524]
    source = source_copies(wrapper)
    suffixes = []
    # Conventional hex digest lengths, kept distinct from evidence of a hash.
    algorithms = {32: ['md5'], 40: ['sha1'], 56: ['sha224'], 64: ['sha256'], 96: ['sha384'], 128: ['sha512']}
    if 'ripemd160' in hashlib.algorithms_available:
        algorithms[40].append('ripemd160')
    digest_trials = []
    for length, names in algorithms.items():
        tail = tokens[-length:]
        start = spans[-length][0]
        union = set(dtokens+tail)
        row = dict(hex_length=length, algorithms=names, start=start, source_chars=len(s)-start,
                   distinct_codes=len(set(tail)), distinct_with_dbbi=len(union),
                   standalone_hex_bijection_possible=len(set(tail)) <= 16,
                   shared_dbbi_hex_bijection_possible=len(union) <= 16,
                   symbols_outside_dbbi=sorted(set(tail)-set(dtokens)), tokens=tail)
        suffixes.append(row)
        if not row['standalone_hex_bijection_possible']:
            continue
        # A very narrow self-checksum model: hash the preceding FAED source or
        # DBBI, using the page decimal representation or raw bytes. No guessed
        # passwords, enciphering keys, arbitrary words, or boundary optimization.
        for operand_name, operand in [('faed_prefix', s[:start]), ('dbbi', d)]:
            for form, raw in integer_forms(operand).items():
                for algorithm in names:
                    digest = hashlib.new(algorithm, raw).hexdigest()
                    mapping = match(tail, digest)
                    digest_trials.append(dict(length=length, start=start, operand=operand_name, form=form,
                                              algorithm=algorithm, digest=digest, mapping=mapping))
    conversions = []
    for start in (522, 523):
        for form, raw in integer_forms(s[start:]).items():
            record = dict(start=start, form=form, byte_length=len(raw), hex=raw.hex())
            if 'integer' in form:
                record['printable_ascii'] = all(32 <= b <= 126 or b in (9, 10, 13) for b in raw)
                record['strict_decodings'] = {}
                for codec in ('utf-8', 'utf-16-le', 'utf-16-be', 'utf-32-le', 'utf-32-be'):
                    try:
                        record['strict_decodings'][codec] = raw.decode(codec)
                    except UnicodeError:
                        pass
            conversions.append(record)
    samples = 20000
    rng = np.random.default_rng(913264)
    controls = {'character_shuffle': [], 'bg_token_shuffle': []}
    for _ in range(samples):
        controls['character_shuffle'].append(float(split_profile(rng.permutation(x))[1].max()))
        perm = rng.permutation(len(tokens))
        y = np.array([ord(c)-97 for i in perm for c in tokens[i]])
        assert np.array_equal(np.bincount(y, minlength=9), np.bincount(x, minlength=9))
        controls['bg_token_shuffle'].append(float(split_profile(y)[1].max()))
    stats = {}
    for name, scores in controls.items():
        exceed = sum(v >= maximum for v in scores)
        p = (exceed+1)/(samples+1)
        stats[name] = dict(samples=samples, exceedances=exceed, empirical_p=p,
                           monte_carlo_standard_error=(p*(1-p)/samples)**.5)
    # Full-length planted checksum validates positive mapping detection.
    synthetic = hashlib.sha1(b'held out complete checksum control').hexdigest()
    mapping = dict(zip('0123456789abcdef', sorted(set(dtokens))))
    planted = [mapping[c] for c in synthetic]
    assert match(planted, synthetic) is not None
    changed = synthetic[:1]+('0' if synthetic[1] != '0' else '1')+synthetic[2:]
    assert match(['a', 'b', 'a'], '010') and match(['a', 'b', 'a'], '011') is None
    summary = dict(status='Exploratory boundary audit; no authenticated plaintext or envelope result',
                   input_sha256=hashlib.sha256(s.encode()).hexdigest(), seed=913264,
                   source_copies=source, best_cut=best, split_statistic=maximum,
                   best_cut_counts=dict(left=dict(Counter(s[:best])), right=dict(Counter(s[best:]))),
                   original_tail=s[best:], whole_token_tail_start=522, whole_token_tail=s[522:],
                   split_inside_bg_token=spans[-40], suffixes=suffixes,
                   digest_trials=len(digest_trials), digest_matches=[r for r in digest_trials if r['mapping']],
                   null_models=stats, controls_passed=True,
                   limitations=['The 523 cut and nearby 522 interpretation were chosen after inspecting data.',
                                'The token-shuffle null is conditional on unverified bg tokenization.',
                                'A tail-specific independent substitution is not excluded by the shared-alphabet contradiction.',
                                'Digest length does not establish hashing; the source explicitly points to SHA256, not SHA1.',
                                'Integer outputs and strict Unicode decodings are retained, not authenticated as plaintext.'])
    (OUT/'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    (OUT/'digest_trials.json').write_text(json.dumps(digest_trials, indent=2), encoding='utf-8')
    (OUT/'integer_outputs.json').write_text(json.dumps(conversions, indent=2), encoding='utf-8')
    (OUT/'null_scores.json').write_text(json.dumps(controls), encoding='utf-8')
    (OUT/'split_profile.json').write_text(json.dumps(dict(cuts=cuts.tolist(), scores=values.tolist())), encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('suffixes', 'source_copies')}, indent=2))
    print(json.dumps(source, indent=2))


if __name__ == '__main__':
    main()
