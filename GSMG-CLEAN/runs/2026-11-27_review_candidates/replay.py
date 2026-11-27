#!/usr/bin/env python3
"""Bounded Cosmic replay for the three reviewer families (profile='gsmg' only).

Usage (from GSMG-CLEAN/):
  python runs/2026-11-27_review_candidates/replay.py build
  python runs/2026-11-27_review_candidates/replay.py grep
  python tools/prereg.py record runs/2026-11-27_review_candidates --outcome passed --evidence runs/2026-11-27_review_candidates/candidates.txt --note "..."
  python runs/2026-11-27_review_candidates/replay.py run
"""
import argparse
import ast
import base64
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from Crypto.Cipher import AES

RUN_DIR = Path(__file__).resolve().parent
GSMG_CLEAN = RUN_DIR.parents[1]
REPO_ROOT = GSMG_CLEAN.parent
TOOLS_DIR = GSMG_CLEAN / 'tools'
sys.path.insert(0, str(TOOLS_DIR))

import check_candidate as cc
import prereg


def load_authenticated_answers():
    """Import authenticated phase answers directly from tools/verify_chain.py without retyping them,
    and assert each one reopens its own envelope / digest."""
    import verify_chain as vc

    # Extract P32 directly from verify_chain.py's AST (open_env(..., <literal>) assigned to p32)
    vc_src = (TOOLS_DIR / 'verify_chain.py').read_text(encoding='utf-8')
    tree = ast.parse(vc_src)
    p32_answer = None
    p2_answer = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            target_name = node.targets[0].id
            if target_name in ('p2', 'p32') and isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Name) and node.value.func.id == 'open_env':
                    arg1 = node.value.args[1]
                    if isinstance(arg1, ast.Constant) and isinstance(arg1.value, str):
                        if target_name == 'p2':
                            p2_answer = arg1.value
                        elif target_name == 'p32':
                            p32_answer = arg1.value

    P1 = vc.first
    P2 = p2_answer
    P3 = ''.join(vc.seven)
    P32 = p32_answer
    CAP = vc.caption
    SLUG = vc.h

    assert isinstance(P1, str) and len(P1) > 0
    assert isinstance(P2, str) and P2 == vc.seven[0]
    assert isinstance(P3, str) and len(P3) == 227
    assert isinstance(P32, str) and len(P32) > 0
    assert isinstance(CAP, str) and len(CAP) > 0
    assert isinstance(SLUG, str) and len(SLUG) == 64

    # Re-assert each authenticated answer opens its own envelope / matches its digest
    p2html = (vc.ORIG / 'pages/phase2_choice.html').read_text(encoding='utf-8')
    ta = vc.textareas(p2html)
    assert vc.open_env(base64.b64decode(ta[0]), P2) == vc.p2, 'P2 failed to reopen phase 2 envelope'
    assert vc.open_env(base64.b64decode(ta[1]), P3) == vc.p3, 'P3 failed to reopen phase 3 envelope'
    i = vc.p3.index(b'U2FsdGVk')
    p32_blob = base64.b64decode(re.sub(rb'\s+', b'', vc.p3[i:]))
    assert vc.open_env(p32_blob, P32) == vc.p32, 'P32 failed to reopen phase 3.2 envelope'
    assert vc.sha(P1.encode()) == '5ac407837447fba24ba2802e4d1e9aecb4580aa29fef1088cc387c180b746f75', 'P1 digest mismatch'
    assert vc.sha(CAP.encode()) == SLUG, 'CAP -> SLUG digest mismatch'
    assert SLUG in (vc.ORIG / 'cdx_wayback_gsmg.json').read_text(encoding='utf-8'), 'SLUG not in CDX'

    return {'P1': P1, 'P2': P2, 'P3': P3, 'P32': P32, 'CAP': CAP, 'SLUG': SLUG}


def build_candidate_rows(ans):
    P1, P2, P3, P32, CAP, SLUG = (ans[k] for k in ('P1', 'P2', 'P3', 'P32', 'CAP', 'SLUG'))
    return [
        # Family 1, cross-phase concatenation (6)
        ('F1_cross_phase', 'P1+P3+P32', P1 + P3 + P32),
        ('F1_cross_phase', 'P1+P2+P3+P32', P1 + P2 + P3 + P32),
        ('F1_cross_phase', 'P3+P32', P3 + P32),
        ('F1_cross_phase', 'P1+P2+P32', P1 + P2 + P32),
        ('F1_cross_phase', 'P1+P3+P32+CAP', P1 + P3 + P32 + CAP),
        ('F1_cross_phase', 'P1+P3+P32+SLUG', P1 + P3 + P32 + SLUG),
        # Family 2, duality text (9)
        ('F2_duality_text', 'theseedisplantedwhenoppositesattract', 'theseedisplantedwhenoppositesattract'),
        ('F2_duality_text', 'whenoppositesattract', 'whenoppositesattract'),
        ('F2_duality_text', 'oppositesattract', 'oppositesattract'),
        ('F2_duality_text', 'The seed is planted when opposites attract', 'The seed is planted when opposites attract'),
        ('F2_duality_text', 'theseedisplantedwhenoppositesattract+P1', 'theseedisplantedwhenoppositesattracttheflowerblossomsthroughwhatseemstobeaconcretesurface'),
        ('F2_duality_text', 'mysteriesoftheunknowncosmicduality', 'mysteriesoftheunknowncosmicduality'),
        ('F2_duality_text', 'Mysteries of the Unknown: Cosmic Duality', 'Mysteries of the Unknown: Cosmic Duality'),
        ('F2_duality_text', '0809465175', '0809465175'),
        ('F2_duality_text', '0809465167', '0809465167'),
        # Family 3, roadmap prefix and phase 2 literals (5)
        ('F3_roadmap_phase2', 'yellowblueprimes_pre_yinyang', 'yellowblueprimesmatrixsumlistlastwordsbeforearchichoice'),
        ('F3_roadmap_phase2', 'phase2_url_slug', 'choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself'),
        ('F3_roadmap_phase2', 'three_urls_concat', 'theseedisplantedchoiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32'),
        ('F3_roadmap_phase2', 'x2sh_literal', '# X 2 S H 4 Y 0 Q B 15 #'),
        ('F3_roadmap_phase2', 'x2sh_compact', 'X2SH4Y0QB15'),
    ]


def cmd_build():
    seal = prereg.verify(RUN_DIR)
    ans = load_authenticated_answers()
    rows = build_candidate_rows(ans)
    assert len(rows) == 20, f'expected 20 candidates, got {len(rows)}'
    cands = [r[2] for r in rows]
    assert len(set(cands)) == 20, 'duplicate candidates'
    for c in cands:
        assert len(c.splitlines()) == 1, f'splitlines breaker in {c!r}'

    cand_bytes = ('\n'.join(cands) + '\n').encode('utf-8')
    (RUN_DIR / 'candidates.txt').write_bytes(cand_bytes)
    cand_sha = hashlib.sha256(cand_bytes).hexdigest()

    prov_lines = ['index\tfamily\tlabel\tcandidate_sha256\tlength\tcandidate']
    for idx, (fam, lbl, s) in enumerate(rows, 1):
        h = hashlib.sha256(s.encode('utf-8')).hexdigest()
        prov_lines.append(f'{idx}\t{fam}\t{lbl}\t{h}\t{len(s)}\t{s}')
    (RUN_DIR / 'provenance.tsv').write_bytes(('\n'.join(prov_lines) + '\n').encode('utf-8'))

    manifest = {
        'prereg_sha256': seal,
        'built_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'count': len(rows),
        'candidates_txt_sha256': cand_sha,
        'authenticated_checks': {
            'P1_sha256': hashlib.sha256(ans['P1'].encode()).hexdigest(),
            'P2_reopened_phase2': True,
            'P3_reopened_phase3': True,
            'P32_reopened_phase3_2': True,
            'CAP_sha256_equals_SLUG_in_CDX': True,
        },
        'rows': [
            {'index': i, 'family': f, 'label': l, 'length': len(s), 'sha256': hashlib.sha256(s.encode()).hexdigest()}
            for i, (f, l, s) in enumerate(rows, 1)
        ],
    }
    (RUN_DIR / 'candidates_manifest.json').write_bytes((json.dumps(manifest, indent=2) + '\n').encode('utf-8'))
    print(f'BUILD OK: {len(rows)} candidates, candidates.txt sha256={cand_sha}')


def cmd_grep():
    cands = (RUN_DIR / 'candidates.txt').read_text(encoding='utf-8').splitlines()
    assert len(cands) == 20
    cand_hashes = {c: hashlib.sha256(c.encode('utf-8')).hexdigest() for c in cands}
    cand_hex = {c: c.encode('utf-8').hex() for c in cands}

    sources = []

    def check_set(name, path_label, strings_set, hashes_set=None):
        hashes_set = hashes_set or set()
        hits = []
        for idx, c in enumerate(cands, 1):
            m = []
            if c in strings_set:
                m.append('exact_string')
            if cand_hashes[c] in hashes_set:
                m.append('sha256_match')
            if m:
                hits.append({'index': idx, 'candidate': c, 'match': m})
        sources.append({'source': name, 'path': path_label, 'entries_checked': len(strings_set) + len(hashes_set), 'hits': hits})

    # 1. gapset_v2
    p = GSMG_CLEAN / 'runs/2026-11-27_cosmic_null_validity/gapset_v2/gap_candidates.txt'
    s = set(p.read_text(encoding='utf-8').splitlines())
    check_set('gapset_v2', str(p.relative_to(REPO_ROOT)).replace('\\', '/'), s)

    # 2. matrixsum_replay forms
    p = GSMG_CLEAN / 'runs/2026-11-27_matrixsum_replay/forms.txt'
    s = set(p.read_text(encoding='utf-8').splitlines())
    check_set('matrixsum_replay_forms', str(p.relative_to(REPO_ROOT)).replace('\\', '/'), s)

    # 3. fefefe_replay
    p = GSMG_CLEAN / 'runs/2026-11-27_fefefe_replay/candidates.txt'
    s = set(p.read_text(encoding='utf-8').splitlines())
    check_set('fefefe_replay', str(p.relative_to(REPO_ROOT)).replace('\\', '/'), s)

    # 4. zero_envelopes (arm_A + arm_C + manifest check)
    zdir = GSMG_CLEAN / 'runs/2026-09-13_zero_envelopes'
    z_strs = set()
    for fn in ('arm_A_candidates.json', 'arm_C_candidates.json'):
        data = json.loads((zdir / fn).read_text(encoding='utf-8'))
        for item in data:
            if isinstance(item, str):
                z_strs.add(item)
            elif isinstance(item, dict):
                for v in item.values():
                    if isinstance(v, str):
                        z_strs.add(v)
    check_set('zero_envelopes_arms_AC', 'GSMG-CLEAN/runs/2026-09-13_zero_envelopes/arm_{A,C}_candidates.json', z_strs)

    # 5. exp2_first_hint_last_command
    e2dir = GSMG_CLEAN / 'runs/2026-09-14_adversarial_reanalysis/exp2_first_hint_last_command'
    e2_rows = json.loads((e2dir / 'results.jsonl.json').read_text(encoding='utf-8'))
    e2_strs = set()
    for r in e2_rows:
        for k in ('text', 'string', 'candidate', 'answer', 'raw_text', 'passphrase'):
            v = r.get(k)
            if isinstance(v, str):
                e2_strs.add(v)
    # Also scan run_exp2.py literals
    e2_src = (e2dir / 'run_exp2.py').read_text(encoding='utf-8')
    e2_hits_src = [c for c in cands if c in e2_src]
    check_set('exp2_first_hint_last_command', 'GSMG-CLEAN/runs/2026-09-14_adversarial_reanalysis/exp2_first_hint_last_command/results.jsonl.json', e2_strs)
    sources[-1]['script_literal_hits'] = e2_hits_src

    # 6. cosmic_six_hash
    c6dir = GSMG_CLEAN / 'runs/2026-11-27_cosmic_six_hash'
    c6_data = json.loads((c6dir / 'results.json').read_text(encoding='utf-8'))
    c6_hashes = {r['inner_sha256'] for r in c6_data.get('rows', []) if 'inner_sha256' in r}
    # Also compute exact inners from tools/cosmic_six_hash.py
    c6_code = (TOOLS_DIR / 'cosmic_six_hash.py').read_text(encoding='utf-8')
    c6_follow = (c6dir / 'followup.txt').read_text(encoding='utf-8')
    c6_strs = set()
    answers6 = ('matrixsumlist', 'lastwordsbeforearchichoice', 'thispassword', 'shabefourfirsthintisyourlastcommand', 'enter', 'shabefanstoo')
    for sep in ('', 'z'):
        for yin in ('', 'yinyang'):
            c6_strs.add(sep.join(answers6) + yin)
    check_set('cosmic_six_hash', 'GSMG-CLEAN/runs/2026-11-27_cosmic_six_hash/results.json', c6_strs, c6_hashes)
    sources[-1]['followup_literal_hits'] = [c for c in cands if c in c6_follow or cand_hashes[c] in c6_follow]

    # 7. gsmg-haiku/review_leads (scan all .py, .json, .jsonl, .txt files for exact strings, sha256s, or hex-encoded answers)
    hr_dir = REPO_ROOT / 'gsmg-haiku/review_leads'
    hr_hits = []
    files_scanned = 0
    for fp in sorted(hr_dir.rglob('*')):
        if not fp.is_file() or fp.suffix not in ('.py', '.json', '.jsonl', '.txt', '.md'):
            continue
        files_scanned += 1
        txt = fp.read_text(encoding='utf-8', errors='ignore')
        for idx, c in enumerate(cands, 1):
            matched_as = []
            if c in txt:
                matched_as.append('exact_string')
            if cand_hashes[c] in txt:
                matched_as.append('sha256_match')
            if cand_hex[c] in txt:
                matched_as.append('answer_hex_match')
            if matched_as:
                hr_hits.append({'index': idx, 'candidate': c, 'file': str(fp.relative_to(REPO_ROOT)).replace('\\', '/'), 'match': matched_as})
    sources.append({
        'source': 'gsmg-haiku_review_leads',
        'path': f'gsmg-haiku/review_leads/** ({files_scanned} files)',
        'entries_checked': files_scanned,
        'hits': hr_hits,
    })

    # Also check seven_key_bifid and last_words_referents (the other two VALID Cosmic nulls in 2026-11-27_cosmic_null_validity)
    skb = GSMG_CLEAN / 'runs/2026-09-13_seven_key_bifid/candidates.json'
    if skb.exists():
        skb_txt = skb.read_text(encoding='utf-8', errors='ignore')
        skb_hits = [{'index': i, 'candidate': c, 'match': ['substring_in_json']} for i, c in enumerate(cands, 1) if f'"{c}"' in skb_txt]
        sources.append({'source': 'seven_key_bifid', 'path': str(skb.relative_to(REPO_ROOT)).replace('\\', '/'), 'entries_checked': 59976, 'hits': skb_hits})

    lwr_dir = GSMG_CLEAN / 'runs/2026-09-13_last_words_referents'
    if lwr_dir.exists():
        lwr_txt = '\n'.join(f.read_text(encoding='utf-8', errors='ignore') for f in lwr_dir.glob('*') if f.is_file())
        lwr_hits = [{'index': i, 'candidate': c, 'match': ['exact_in_dir']} for i, c in enumerate(cands, 1) if c in lwr_txt]
        sources.append({'source': 'last_words_referents', 'path': 'GSMG-CLEAN/runs/2026-09-13_last_words_referents/*', 'entries_checked': 15676, 'hits': lwr_hits})

    out = {
        'grepped_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'candidates_count': len(cands),
        'sources': sources,
        'total_hits': sum(len(x['hits']) for x in sources),
    }
    (RUN_DIR / 'coverage_grep.json').write_bytes((json.dumps(out, indent=2) + '\n').encode('utf-8'))
    print(f'GREP DONE: total hits across all checked sources = {out["total_hits"]}')
    for x in sources:
        print(f'  {x["source"]:30s}: hits={len(x["hits"])} ({x["path"]})')
        for h in x['hits']:
            print('    HIT:', h)


def printable_fraction(pt: bytes) -> float:
    if not pt:
        return 0.0
    return sum((b in (9, 10, 13)) or (32 <= b < 127) for b in pt) / len(pt)


def encrypt_gsmg_envelope(plaintext: bytes, answer: str, salt: bytes) -> bytes:
    """Encrypt a synthetic Salted__ envelope under profile 'gsmg' for the planted control."""
    assert len(salt) == 8
    pw, md = cc.PROFILES['gsmg'](answer)
    key, iv = cc.evp(pw, salt, md)
    pad = 16 - (len(plaintext) % 16)
    padded = plaintext + bytes([pad]) * pad
    ct = AES.new(key, AES.MODE_CBC, iv).encrypt(padded)
    return b'Salted__' + salt + ct


def decrypt_and_scan(envelopes: dict, candidates: list, out_dir: Path):
    """Single shared decryption + retention + key-scan loop used for both planted control and real run."""
    out_dir.mkdir(parents=True, exist_ok=True)
    histograms = {name: {'decrypts': 0, 'pad_0': 0, 'pad_1': 0, 'pad_2': 0, 'pad_ge3': 0} for name in envelopes}
    retained = []
    dbbi_matches = []

    for idx, ans in enumerate(candidates, 1):
        if cc.eq_pattern(hashlib.sha256(ans.encode()).hexdigest()) == cc.DBBI_PATTERN:
            dbbi_matches.append({'index': idx, 'answer': ans})
        for env_name, raw in envelopes.items():
            histograms[env_name]['decrypts'] += 1
            pad, pt = cc.try_envelope(raw, ans, 'gsmg')
            if pad == 0:
                histograms[env_name]['pad_0'] += 1
                continue
            if pad == 1:
                histograms[env_name]['pad_1'] += 1
            elif pad == 2:
                histograms[env_name]['pad_2'] += 1
            else:
                histograms[env_name]['pad_ge3'] += 1

            env_out = out_dir / env_name
            env_out.mkdir(parents=True, exist_ok=True)
            bin_path = env_out / f'cand_{idx:02d}.bin'
            bin_path.write_bytes(pt)

            pfrac = printable_fraction(pt)
            keys = cc.find_keys(pt)
            hits = [{'kind': d, 'targets': h} for d, h in keys if h]
            rec = {
                'envelope': env_name,
                'candidate_index': idx,
                'candidate': ans,
                'pad': pad,
                'plaintext_len': len(pt),
                'plaintext_sha256': hashlib.sha256(pt).hexdigest(),
                'printable_fraction': round(pfrac, 6),
                'bin_file': str(bin_path.relative_to(RUN_DIR)).replace('\\', '/'),
                'find_keys_hits': hits,
                'preview_200_hex': pt[:200].hex(),
            }
            if pfrac > 0.85:
                rec['preview_200_text'] = pt[:200].decode('latin1')
            retained.append(rec)

    return histograms, retained, dbbi_matches


def cmd_run():
    # 1. Verify preregistration seal AND bound candidates.txt BEFORE any decrypt
    seal = prereg.verify(RUN_DIR)
    sc_path = RUN_DIR / 'SELFCHECK.json'
    assert sc_path.exists(), 'SELFCHECK.json missing: run prereg.py record first'
    sc = json.loads(sc_path.read_text(encoding='utf-8'))
    assert sc['prereg_sha256'] == seal, 'SELFCHECK seal mismatch'
    assert sc['outcome'] == 'passed', 'SELFCHECK not passed'
    cand_path = RUN_DIR / 'candidates.txt'
    cand_sha = hashlib.sha256(cand_path.read_bytes()).hexdigest()
    assert cand_sha == sc['evidence_sha256'], 'candidates.txt changed after prereg record'

    candidates = cand_path.read_text(encoding='utf-8').splitlines()
    assert len(candidates) == 20, f'expected 20 candidates, got {len(candidates)}'

    # 2. Control 1: cc.selftest() (must reopen Phase 3.2)
    cc.selftest()

    # 3. Control 2: planted Salted__ envelope encrypted under profile 'gsmg' containing planted k=1 key
    planted_answer = 'planted_control_review_candidates_2026_11_27'
    planted_salt = bytes.fromhex('0102030405060708')
    planted_pt = (
        b'CONTROL OK '
        + (1).to_bytes(32, 'big')
        + b' WIF=5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf HEX='
        + b'0' * 63 + b'1'
    )
    planted_env = encrypt_gsmg_envelope(planted_pt, planted_answer, planted_salt)
    expected_pad = 16 - (len(planted_pt) % 16)

    k1_h160 = '91b24bf9f5288532960ac687abb035127b1d28a5'
    cc.TARGETS[k1_h160] = 'PLANTED CONTROL k=1'
    try:
        ctrl_hist, ctrl_ret, _ = decrypt_and_scan(
            {'planted_control': planted_env},
            [planted_answer] + candidates,
            RUN_DIR / 'controls',
        )
    finally:
        del cc.TARGETS[k1_h160]

    assert set(cc.TARGETS.keys()) == {
        'a9553269572a317e39f0f518cb87c1a0ee1dbae4',
        '4bc468447fe1b048ad030a2f9a125478eabc4ed6',
    }, 'cc.TARGETS not cleanly restored to Half + Better Half'

    planted_hits = [r for r in ctrl_ret if r['candidate'] == planted_answer]
    assert len(planted_hits) == 1, f'planted control failed to open: {ctrl_ret}'
    ph = planted_hits[0]
    assert ph['pad'] == expected_pad, f'planted pad mismatch: {ph["pad"]} != {expected_pad}'
    assert (RUN_DIR / ph['bin_file']).read_bytes() == planted_pt, 'planted plaintext byte mismatch'
    found_kinds = {h['kind'].split('@')[0] for h in ph['find_keys_hits']}
    assert found_kinds == {'raw32', 'WIF', 'hex64'}, f'planted find_keys failed: {ph["find_keys_hits"]}'

    # 4. Real bounded run: 20 candidates x 3 cc.ENVELOPES, profile 'gsmg' ONLY
    assert set(cc.ENVELOPES.keys()) == {'terminal_phase3_2_end', 'salphaseion_short', 'cosmic_duality'}
    real_hist, real_ret, real_dbbi = decrypt_and_scan(cc.ENVELOPES, candidates, RUN_DIR / 'outputs')

    total_decrypts = sum(v['decrypts'] for v in real_hist.values())
    total_key_hits = sum(len(r['find_keys_hits']) for r in real_ret)
    total_pad_ge3 = sum(v['pad_ge3'] for v in real_hist.values())
    high_printable = [r for r in real_ret if r['printable_fraction'] > 0.85]
    verdict = 'HIT' if (total_key_hits > 0 or total_pad_ge3 > 0 or len(high_printable) > 0) else 'NULL'

    results = {
        'run_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'prereg_sha256': seal,
        'candidates_txt_sha256': cand_sha,
        'profile': 'gsmg',
        'candidates_count': len(candidates),
        'envelopes': {
            n: {'bytes': len(b), 'salt': b[8:16].hex(), 'sha256': hashlib.sha256(b).hexdigest()}
            for n, b in cc.ENVELOPES.items()
        },
        'controls': {
            'cc_selftest': 'PASSED',
            'planted_control': {
                'answer': planted_answer,
                'expected_pad': expected_pad,
                'observed_pad': ph['pad'],
                'plaintext_exact_match': True,
                'find_keys_kinds_fired': sorted(found_kinds),
                'histogram': ctrl_hist['planted_control'],
                'extra_chance_hits': [r for r in ctrl_ret if r['candidate'] != planted_answer],
            },
            'targets_verified': cc.TARGETS,
        },
        'total_decrypts': total_decrypts,
        'histograms': real_hist,
        'dbbi_pattern_matches': real_dbbi,
        'retained_pad_valid_count': len(real_ret),
        'retained': real_ret,
        'total_key_hits': total_key_hits,
        'high_printable_count': len(high_printable),
        'verdict': verdict,
    }
    (RUN_DIR / 'results.json').write_bytes((json.dumps(results, indent=2) + '\n').encode('utf-8'))
    print(f'RUN COMPLETE: {total_decrypts} decrypts, retained={len(real_ret)}, key_hits={total_key_hits}, pad>=3={total_pad_ge3}, verdict={verdict}')
    for n, h in real_hist.items():
        print(f'  {n:25s}: {h}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=('build', 'grep', 'run'))
    a = ap.parse_args()
    if a.cmd == 'build':
        cmd_build()
    elif a.cmd == 'grep':
        cmd_grep()
    else:
        cmd_run()
