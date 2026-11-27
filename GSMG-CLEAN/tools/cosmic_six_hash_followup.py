#!/usr/bin/env python3
"""Follow-up on the Cosmic six-answer run.

Shows the password path for rows 07, 15, 23 and 31, then runs the Half
uncompressed public key through the same hash and format variants. Writes
GSMG-CLEAN/runs/2026-11-27_cosmic_six_hash/followup.txt. Decrypt previews are
included only for a padding hit or a printable-ASCII ratio above 0.42.
"""
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cosmic_six_hash as cosmic  # noqa: E402
import prize_gate as pg  # noqa: E402

OUT = cosmic.OUT / 'followup.txt'
ROW_NUMBERS = (7, 15, 23, 31)
RATIO_MARK = 0.42


def notable(pad, ratio):
    return pad or ratio > RATIO_MARK


def line_for(label, pad, ratio, plain):
    text = f'{label} pad={"Y" if pad else "N"} printable_ascii={ratio:.4f}'
    if notable(pad, ratio):
        kind, shown = cosmic.preview(plain)
        text += f'\npreview={kind}\n{shown}'
    return text


def main():
    cosmic.verify_phase32()
    blob = cosmic.verify_cosmic()
    rows = cosmic.candidates()
    if len(rows) != 32:
        raise SystemExit(f'expected 32 candidates, built {len(rows)}')

    lines = []
    lines.append('phase 3.2 control: PASS')
    lines.append('sha256-hex passphrase, EVP_BytesToKey SHA-256, plaintext matches phase3_2_plaintext.bin')
    lines.append('')
    lines.append('rows 07, 15, 23, 31 code path')
    lines.append('body = inner.encode()')
    lines.append('single = SHA-256(body)')
    lines.append('doubled = SHA-256(single)')
    lines.append('password = doubled.hex().encode()  # 64 lowercase ASCII chars')
    lines.append('EVP_BytesToKey(password, salt, md=MD5, 1 iteration), AES-256-CBC')
    lines.append('md=md5 is the KDF digest. The password hash is SHA-256 twice, not MD5.')
    lines.append('MD5-then-SHA256 cells were not run.')
    lines.append('')

    hashed_md5_twice = False
    for number in ROW_NUMBERS:
        row = rows[number - 1]
        body = row['inner'].encode()
        single = hashlib.sha256(body).digest()
        doubled = hashlib.sha256(single).digest()
        password = doubled.hex().encode()
        md5_twice = hashlib.md5(hashlib.md5(body).digest()).hexdigest().encode()
        if row['password'] != password or row['rounds'] != 2 or row['form'] != 'hex-lower' or row['md'] != 'md5':
            raise SystemExit(f'row {number:02d} is not SHA-256 twice as lowercase hex under EVP-MD5')
        if row['password'] == md5_twice:
            hashed_md5_twice = True
        lines.append(
            f"{number:02d} sep={row['separator']} yin={row['yinyang']} "
            f'inner_len={len(body)} password_sha256={hashlib.sha256(password).hexdigest()}'
        )
    if hashed_md5_twice:
        raise SystemExit('row password matched MD5 twice; the follow-up grid was not coded for that')
    lines.append('')

    sources = (
        ('pubkey-bytes', pg.HALF_PUBLIC_UNCOMPRESSED),
        ('pubkey-hex', pg.HALF_PUBLIC_UNCOMPRESSED.hex().encode()),
    )
    if pg.HALF_PUBLIC_UNCOMPRESSED.hex() != (
        '04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4'
        '649c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559'
    ):
        raise SystemExit('Half uncompressed pubkey drifted')
    tested = 0
    hits = []
    marked = []
    for source_name, body in sources:
        for form, password, rounds in cosmic.password_forms(body):
            for md_name, md in (('md5', hashlib.md5), ('sha256', hashlib.sha256)):
                plain = cosmic.decrypt_raw(blob, password, md)
                pad = cosmic.pkcs7_valid(plain)
                ratio = cosmic.printable_ratio(plain)
                tested += 1
                label = f'half source={source_name} form={form} rounds={rounds} md={md_name}'
                text = line_for(label, pad, ratio, plain)
                if pad:
                    hits.append(text)
                if ratio > RATIO_MARK:
                    marked.append(text)
    lines.append('half key sources: pubkey-bytes (65-byte uncompressed), pubkey-hex (130-char lowercase hex)')
    lines.append('variants: hex-lower, raw, hex-upper, and SHA-256 twice as hex-lower; EVP-MD5 and EVP-SHA256')
    lines.append(f'half key tested: {tested}')
    lines.append('padding hits:')
    lines.extend(hits or ['none'])
    lines.append(f'printable ratio above {RATIO_MARK:.2f}:')
    lines.extend(marked or ['none'])
    if not marked:
        lines.append('no hex preview')

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(OUT.read_text())


if __name__ == '__main__':
    main()
