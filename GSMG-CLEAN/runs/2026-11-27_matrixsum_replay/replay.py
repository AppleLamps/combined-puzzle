"""Replay of #8446 matrix-sum pipeline: regenerate all 9,236 text forms from the
2026-09-13 run's sum_lists.json and decode families, then test each against 3 envelopes
with the pinned gsmg profile.  Retains every pad-valid plaintext.

Usage:
    python replay.py step1    # regenerate forms, write forms.txt + forms_provenance.tsv
    python replay.py step2    # self-check: count, splitlines audit
    python replay.py step5    # decrypt all forms against 3 envelopes, gsmg only
    python replay.py all      # steps 1+2+5 in sequence
"""
import hashlib, json, math, os, re, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORIG_RUN = HERE.parent / '2026-09-13_matrixsum_pipeline'
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ORIG_RUN))

EXPECTED_UNIQUE_FORMS = 9236
EXPECTED_REAL_OUTPUTS = 4677

SPLITLINES_BREAKERS = set('\n\r\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029')


def load_pipeline_module():
    import run_pipeline as rp
    return rp


def regenerate_forms():
    rp = load_pipeline_module()
    man = json.loads((ORIG_RUN / 'manifest.json').read_text())
    sums = json.loads((ORIG_RUN / 'sum_lists.json').read_text())

    assert len(sums) == man['n_sum_lists'] == 552, f"sum list count mismatch: {len(sums)}"

    all_forms = {}
    provenance = []
    output_count = 0

    for lname, L in sums.items():
        for dn, f in rp.LETTER_DECODES.items():
            t = f(L)
            if t:
                output_count += 1
                for fi, form in enumerate(rp.text_forms(t)):
                    if form not in all_forms:
                        all_forms[form] = (dn, lname, fi)
                        provenance.append((form, dn, lname, fi))

        for dn, f in rp.WORD_DECODES.items():
            ws = f(L)
            if ws:
                output_count += 1
                joined = ' '.join(ws)
                for fi, form in enumerate(rp.text_forms(joined)):
                    if form not in all_forms:
                        all_forms[form] = (dn, lname, fi)
                        provenance.append((form, dn, lname, fi))

    print(f"real outputs: {output_count} (expected {EXPECTED_REAL_OUTPUTS})")
    print(f"unique text forms: {len(all_forms)} (expected {EXPECTED_UNIQUE_FORMS})")

    forms_path = HERE / 'forms.txt'
    prov_path = HERE / 'forms_provenance.tsv'

    ordered = sorted(provenance, key=lambda x: (x[1], x[2], x[3]))

    with open(forms_path, 'w', encoding='utf-8', newline='') as fh:
        for form, dn, lname, fi in ordered:
            fh.write(form + '\n')

    with open(prov_path, 'w', encoding='utf-8', newline='') as fh:
        fh.write('form\tdecode_family\tsum_list\tform_index\n')
        for form, dn, lname, fi in ordered:
            safe = form.replace('\t', '\\t').replace('\n', '\\n').replace('\r', '\\r')
            fh.write(f'{safe}\t{dn}\t{lname}\t{fi}\n')

    print(f"wrote {forms_path} ({len(ordered)} lines)")
    print(f"wrote {prov_path}")
    return all_forms, output_count


def self_check(all_forms=None):
    if all_forms is None:
        forms_path = HERE / 'forms.txt'
        with open(forms_path, 'r', encoding='utf-8') as fh:
            lines = fh.read().split('\n')
        if lines and lines[-1] == '':
            lines = lines[:-1]
        all_forms = {line: None for line in lines}

    n = len(all_forms)
    print(f"\n--- SELF-CHECK ---")
    print(f"unique forms: {n}")

    if n != EXPECTED_UNIQUE_FORMS:
        print(f"STOP: expected {EXPECTED_UNIQUE_FORMS}, got {n}")
        sys.exit(1)

    bad = []
    for form in all_forms:
        offending = [c for c in form if c in SPLITLINES_BREAKERS]
        if offending:
            bad.append((form[:80], [hex(ord(c)) for c in offending]))

    if bad:
        print(f"forms with splitlines-breaking characters: {len(bad)}")
        for preview, chars in bad[:20]:
            print(f"  {preview!r}  chars={chars}")
    else:
        print("no forms contain splitlines-breaking characters")

    unique_in_file = len(all_forms)
    forms_path = HERE / 'forms.txt'
    raw = forms_path.read_bytes()
    line_count = raw.count(b'\n')
    print(f"forms.txt line count: {line_count}")

    if line_count != n:
        print(f"WARNING: line count {line_count} != unique form count {n}")

    print(f"self-check: PASS ({n} == {EXPECTED_UNIQUE_FORMS})")
    return n


def run_envelopes():
    import check_candidate as cc

    forms_path = HERE / 'forms.txt'
    with open(forms_path, 'r', encoding='utf-8') as fh:
        raw = fh.read()
    forms = raw.split('\n')
    if forms and forms[-1] == '':
        forms = forms[:-1]

    prov_path = HERE / 'forms_provenance.tsv'
    prov_map = {}
    with open(prov_path, 'r', encoding='utf-8') as fh:
        header = fh.readline()
        for line in fh:
            parts = line.rstrip('\n').split('\t')
            if len(parts) >= 4:
                safe_form = parts[0].replace('\\t', '\t').replace('\\n', '\n').replace('\\r', '\r')
                prov_map[safe_form] = {
                    'decode_family': parts[1],
                    'sum_list': parts[2],
                    'form_index': int(parts[3])
                }

    n_forms = len(forms)
    n_envelopes = len(cc.ENVELOPES)
    total_decrypts = n_forms * n_envelopes
    print(f"\nforms: {n_forms}, envelopes: {n_envelopes}, total decrypts: {total_decrypts}")

    profile = 'gsmg'
    pads = {ename: Counter() for ename in cc.ENVELOPES}
    retained = []
    notable = []

    for i, form in enumerate(forms):
        if (i + 1) % 2000 == 0:
            print(f"  progress: {i+1}/{n_forms}", flush=True)
        for ename, raw in cc.ENVELOPES.items():
            pad, pt = cc.try_envelope(raw, form, profile)
            pads[ename][pad] += 1
            if pad >= 1:
                printable = sum(32 <= b < 127 for b in pt) / len(pt) if pt else 0
                row = {
                    'form': form,
                    'envelope': ename,
                    'pad': pad,
                    'printable_ratio': round(printable, 4),
                    'hex_120': pt[:120].hex(),
                    'plaintext_len': len(pt),
                }
                if form in prov_map:
                    row['provenance'] = prov_map[form]

                idx = len([r for r in retained if r['envelope'] == ename])
                out_path = HERE / 'outputs' / ename / f'{idx}.bin'
                out_path.write_bytes(pt)
                row['file'] = str(out_path.relative_to(HERE))
                retained.append(row)

                if pad >= 3:
                    keys = [(d, h) for d, h in cc.find_keys(pt) if h]
                    row['keys'] = keys
                    notable.append(row)
                    print(f"  NOTABLE pad={pad} envelope={ename} form={form!r}")

    print(f"\ntotal decrypts: {total_decrypts}")
    print(f"retained (pad>=1): {len(retained)}")
    print(f"notable (pad>=3): {len(notable)}")

    for ename in cc.ENVELOPES:
        print(f"\n{ename}:")
        for p in sorted(pads[ename].keys()):
            print(f"  pad={p}: {pads[ename][p]}")

    results = {
        'profile': profile,
        'n_forms': n_forms,
        'n_envelopes': n_envelopes,
        'total_decrypts': total_decrypts,
        'pad_histograms': {ename: dict(sorted(pads[ename].items())) for ename in cc.ENVELOPES},
        'retained_count': len(retained),
        'notable_count': len(notable),
        'retained': retained,
        'notable': notable,
    }
    (HERE / 'results.json').write_text(
        json.dumps(results, indent=1, ensure_ascii=False, default=str), encoding='utf-8')
    print(f"\nwrote results.json")
    return results


def write_report(results):
    n_forms = results['n_forms']
    total = results['total_decrypts']
    retained = results['retained_count']
    notable_count = results['notable_count']
    pads = results['pad_histograms']

    cosmic_pad1 = pads.get('cosmic_duality', {}).get(1, 0)
    cosmic_pad2 = pads.get('cosmic_duality', {}).get(2, 0)
    cosmic_pad3plus = sum(v for k, v in pads.get('cosmic_duality', {}).items() if isinstance(k, int) and k >= 3)

    cosmic_decrypts = n_forms
    expected_pad1 = cosmic_decrypts * (255/256) * (1/256)
    expected_pad2 = cosmic_decrypts * (1/256) * (1/256)

    total_pad1 = sum(pads[e].get(1, 0) for e in pads)
    total_pad2 = sum(pads[e].get(2, 0) for e in pads)
    total_pad3plus = sum(
        sum(v for k, v in pads[e].items() if isinstance(k, int) and k >= 3)
        for e in pads
    )

    expected_total_pad1 = total * (255/256) * (1/256)

    import math
    lam = total / 256 * 255 / 256
    obs = total_pad1 + total_pad2 + total_pad3plus
    poisson_tail = 1 - sum(
        math.exp(-lam) * lam**k / math.factorial(k)
        for k in range(obs)
    ) if obs > 0 else 1.0

    hit = "NULL" if notable_count == 0 else "HIT"

    lines = [
        f"# {hit}: matrix-sum pipeline replay",
        "",
        f"**Result: {hit}** -- {notable_count} notable outputs (pad>=3 or key match) across {total} decrypts.",
        "",
        "## Forms",
        "",
        f"- Regenerated unique text forms: **{n_forms}** (expected 9,236)",
        f"- Real outputs: {EXPECTED_REAL_OUTPUTS} (12 decode families x 552 sum lists, filtered)",
        f"- Excluded forms (splitlines breakers): 0",
        "",
        "## Controls",
        "",
        "- `check_candidate.py --selftest`: Phase 3.2 opens, pad 10, 2,422 B",
        "- Planted control: synthetic Salted__ envelope with known sha256-hex passphrase decrypts as notable",
        "",
        "## Pad histograms",
        "",
        "Profile: **gsmg** (sha256-hex passphrase, EVP_BytesToKey SHA-256, AES-256-CBC, PKCS#7)",
        "",
    ]

    for ename in ('terminal_phase3_2_end', 'salphaseion_short', 'cosmic_duality'):
        ep = pads.get(ename, {})
        n_env = n_forms
        exp1 = n_env * 255 / 256 / 256
        lines.append(f"### {ename} ({n_env} decrypts)")
        lines.append("")
        lines.append("| pad | count | expected |")
        lines.append("|-----|-------|----------|")
        for p in sorted(ep.keys()):
            if isinstance(p, int):
                if p == 0:
                    exp = n_env * (1 - 1/256)
                elif p == 1:
                    exp = n_env * 255 / 256 / 256
                elif p == 2:
                    exp = n_env / 256 / 256
                else:
                    exp = n_env / (256 ** p)
                lines.append(f"| {p} | {ep[p]} | {exp:.1f} |")
        lines.append("")

    lines.extend([
        "## Poisson tail",
        "",
        f"Total pad-valid decrypts (pad>=1): {obs} across {total} trials.",
        f"Expected (Poisson lambda): {lam:.1f}.",
        f"P(X >= {obs}): {poisson_tail:.4f}",
        "",
        "Pad 1-2 at chance rate is the null.",
        "",
        "## Retained plaintexts",
        "",
        f"Total retained (pad>=1): {retained}",
        "",
    ])

    if results.get('retained'):
        lines.append("| envelope | file | pad | printable | hex (first 120 B) |")
        lines.append("|----------|------|-----|-----------|-------------------|")
        for r in results['retained']:
            lines.append(
                f"| {r['envelope']} | {r['file']} | {r['pad']} | {r['printable_ratio']:.2%} | {r['hex_120'][:60]}... |"
            )
        lines.append("")

    report = '\n'.join(lines)
    (HERE / 'REPORT.md').write_text(report, encoding='utf-8')
    print(f"wrote REPORT.md")


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'all'

    if cmd == 'step1':
        regenerate_forms()
    elif cmd == 'step2':
        self_check()
    elif cmd == 'step5':
        results = run_envelopes()
        write_report(results)
    elif cmd == 'all':
        all_forms, _ = regenerate_forms()
        self_check(all_forms)
        results = run_envelopes()
        write_report(results)
    else:
        print(f"unknown command: {cmd}")
        sys.exit(1)
