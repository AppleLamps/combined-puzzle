#!/usr/bin/env python3
"""
Reproducible check of the 'btcseed' Bifid finding (SalPhaseIon SEG-0/SEG-1).

Claim in the group (June 2025 onward): decoding the faed... string as a Bifid
cipher, period 570, keyed by the deduplicated head of the dbbi... string,
yields plaintext beginning "btcseed" -- odds quoted in chat as 1 in 8,031,810,176.

This script reproduces the result and then measures how special it actually is.
Run: python3 verify_btcseed.py
"""
import itertools, collections

DBBI = ("dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbee"
        "ggecbedcibfbffgigbeeeabe")
FAED = ("faedggeedfcbdabhhggcadcfeddgfdgbgigaaedggiafaecghggcdaihehahbahigce"
        "ifgbfgefgaifabifagaegeacgbbeagfggeeggafbacgfcdbeiffaafcidahgdeefghh"
        "cggaegdebhhegeghcegadfbdiagefcicggifdcgaaggfbigaicfbhecaecbceiaiceb"
        "gbgiecdeggfgegaedggfiiciiififhggcgfgdcdggefcbeeigefibgibggghhfbcgif"
        "dehedfdagicdbhicgaiedaehahghhcihdghfhbiicecbiichihiiigiddgehhdfdchc"
        "bafgfbhaheagegecafehgcfggggcagfhhghbaihidiehhfdeggdgcihggggghadahig"
        "igbgecgedfcdggaccdehiicigfbffhggaeidbbeibbeiifdgfdhieeeieeecifdgdah"
        "diggfhegfiaffiggbcbcehceabfbedbiibfbfdedeehgigfaaiggagbeiichiedifbe"
        "hgbccahhbiibibbibdcbahaidhfahiihic")
KEY = "dbifhceg"          # dbbi head, deduplicated
PERIOD = len(FAED)        # 570


def square(kw):
    seen = []
    for c in kw + "abcdefghiklmnopqrstuvwxyz":
        c = 'i' if c == 'j' else c
        if c not in seen:
            seen.append(c)
    return seen


def bifid_decode(ct, kw, period):
    sq = square(kw)
    pos = {c: (i // 5, i % 5) for i, c in enumerate(sq)}
    out = []
    for i in range(0, len(ct), period):
        blk = ct[i:i + period]
        seq = []
        for c in blk:
            r, col = pos[c]
            seq += [r, col]
        n = len(blk)
        rows, cols = seq[:n], seq[n:]
        out.append(''.join(sq[rows[j] * 5 + cols[j]] for j in range(n)))
    return ''.join(out)


def main():
    plain = bifid_decode(FAED, KEY, PERIOD)
    print("1. REPRODUCTION")
    print(f"   output[:32] = {plain[:32]}")
    print(f"   starts with 'btcseed': {plain.startswith('btcseed')}\n")

    print("2. HOW RARE IS IT? (all 8! = 40320 orderings of the same key letters)")
    seed_hits, exact, prefixes = 0, 0, collections.Counter()
    for p in itertools.permutations(KEY):
        r = bifid_decode(FAED, ''.join(p), PERIOD)
        if "seed" in r[:8]:
            seed_hits += 1
            prefixes[r[:7]] += 1
        if r[:7] == "btcseed":
            exact += 1
    n = 40320
    print(f"   keys yielding 'seed' in first 8 chars : {seed_hits}/{n} = {100*seed_hits/n:.2f}%")
    print(f"   keys yielding exactly 'btcseed'       : {exact}")
    print(f"   quoted odds in chat                   : 1 in 8,031,810,176")
    print("   other prefixes produced by sibling keys:",
          ', '.join(k for k, _ in prefixes.most_common(8)), "\n")

    print("3. IS THE 'STRUCTURE' IN THE TAIL REAL? (alternating-position alphabet)")
    for kw in [KEY, "abcdefghi", "hgfedcbai", "qwertyuio", "zyxwvutsr"]:
        sl = bifid_decode(FAED, kw, PERIOD)[8::2]
        c = collections.Counter(sl)
        print(f"   key={kw:10s} distinct letters at alternating positions = {len(c):2d} "
              f"-> {sorted(c)[:6]}")
    print("\n   The '4 states / 96-state object / 281 states' structure appears for")
    print("   nonsense keys too. It is an artifact of Bifid-decoding a 9-letter")
    print("   alphabet at period = ciphertext length, not a message.")


if __name__ == "__main__":
    main()
