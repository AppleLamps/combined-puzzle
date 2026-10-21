"""Recompute four unattributed on-chain uncompressed neighbor addresses from P."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib


def check(name, ok):
    print(('PASS ' if ok else 'FAIL ') + name)
    if not ok:
        raise AssertionError(name)


def main():
    p = lib.PRIZE_POINT
    curve = lib.SECP256K1_P
    check('prize point on secp256k1', (p[1] * p[1] - p[0] ** 3 - 7) % curve == 0)
    check('prize uncompressed HASH160', lib.h160(lib.uncompressed_point(p)) == lib.PRIZE_H160)
    check('prize P2PKH address', lib.p2pkh_address(lib.uncompressed_point(p)) ==
          '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe')
    points = lib.related_public_points(p)
    for relation, expected in lib.RELATED_ADDRESSES.items():
        check(relation + ' on curve',
              (points[relation][1] ** 2 - points[relation][0] ** 3 - 7) % curve == 0)
        check(relation + ' uncompressed address',
              lib.p2pkh_address(lib.uncompressed_point(points[relation])) == expected)
        check(relation + ' is not prize', points[relation] != p)
    check('minus_one + G == P', lib.point_add(points['minus_one'], lib.GENERATOR) == p)
    check('half + half == P', lib.point_add(points['half'], points['half']) == p)
    check('double == P + P', points['double'] == lib.point_add(p, p))
    check('plus_one - G == P', lib.point_add(
        points['plus_one'],
        (lib.GENERATOR[0], -lib.GENERATOR[1] % curve)) == p)
    check('scalar one control: 1G = G', lib.point_mul(lib.GENERATOR, 1) == lib.GENERATOR)
    check('scalar group order control: nG = infinity',
          lib.point_mul(lib.GENERATOR, lib.SECP256K1_N) is None)
    check('scalar normalization formulas', all(
        int.from_bytes(lib.normalize_related_scalar(
            (fn(12345) % lib.SECP256K1_N).to_bytes(32, 'big'), relation), 'big') == 12345
        for relation, fn in {
            'minus_one': lambda d: d - 1, 'half': lambda d: d * pow(2, -1, lib.SECP256K1_N),
            'double': lambda d: d * 2, 'plus_one': lambda d: d + 1,
        }.items()))
    print('SUMMARY: key relations verified (public data only)')


if __name__ == '__main__':
    main()
