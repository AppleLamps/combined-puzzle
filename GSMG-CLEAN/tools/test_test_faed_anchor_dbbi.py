import unittest

import test_faed_anchor_dbbi as m


class AnchorDbbiTests(unittest.TestCase):
    def test_anchor_characters(self):
        faed = (m.DATA / "FAED_570.txt").read_text().strip()
        self.assertEqual([faed[i] for i in (5, 479, 484)], list("gag"))
        self.assertEqual([faed[i-1] for i in (5, 479, 484)], list("gig"))

    def test_complete_accounting_and_roundtrip(self):
        manifest, rows = m.build()
        self.assertEqual(manifest["candidate_count"], 1040)
        self.assertTrue(rows)
        self.assertTrue(all(r["ordinary_roundtrip"] for r in rows))
        self.assertEqual({(r["parse_cells"], r["ordinary_count"]) for r in rows},
                         {(84, 61), (83, 60)})

    def test_neighborhood(self):
        self.assertEqual(m.neighborhood("abcdefghi", 4, 2, False), "cdefg")
        self.assertEqual(m.neighborhood("abcdefghi", 4, 2, True), "gfedc")

    def test_prime_modes_are_bounded(self):
        for mode in ("replace", "add", "subtract", "reverse_subtract", "xor"):
            for a in range(1, 10):
                for b in range(1, 10):
                    self.assertIn(m.transform(a, b, mode), range(1, 10))

    def test_bifid_control(self):
        dbbi = (m.DATA / "DBBI_91.txt").read_text().strip()
        faed = (m.DATA / "FAED_570.txt").read_text().strip()
        self.assertTrue(m.bifid_decode(faed, dbbi).startswith("btcseed"))

    def test_sum_renderings(self):
        got = m.sum_renderings({"1x2": {"rows": [27], "columns": [1, 26]}})
        self.assertEqual(got["1x2"]["columns"]["mod26_A1"], "az")


if __name__ == "__main__":
    unittest.main()
