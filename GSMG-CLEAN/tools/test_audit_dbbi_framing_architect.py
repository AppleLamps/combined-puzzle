import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import audit_dbbi_framing_architect as audit


class FramingTests(unittest.TestCase):
    def setUp(self):
        self.framing = audit.load_framing()

    def test_exact_accounting(self):
        self.assertEqual(len(self.framing["cells"]), 83)
        self.assertEqual(len(self.framing["markers"]), 23)
        self.assertEqual(len(self.framing["gaps"]), 24)
        self.assertEqual(sum(map(len, self.framing["gaps"])), 60)
        self.assertEqual("".join(map("".join, self.framing["gaps"])), self.framing["payload"])

    def test_known_gap_lengths(self):
        self.assertEqual(
            self.framing["lengths"],
            [1, 0, 1, 1, 3, 1, 3, 1, 3, 5, 1, 5, 3, 1, 3, 5, 5, 1, 5, 3, 1, 5, 3, 0],
        )

    def test_marker_values_never_enter_payload(self):
        offsets = {m["offset"] for m in self.framing["markers"]}
        self.assertEqual(self.framing["schedule"], "BBBBYBBBYYBBBBYBBYYBBYY")
        self.assertTrue(offsets)
        self.assertEqual(self.framing["payload"], "difhccgihaeeihggegebgehhehhfafdhffcdbfcccgfeggecdcifffgigeea")

    def test_reversal_preserves_boundaries_and_multiset(self):
        for mode in ("none", "all", "blue", "yellow"):
            for attachment in ("closes", "opens"):
                gaps = audit.reverse_gaps(self.framing["gaps"], self.framing["schedule"], mode, attachment)
                self.assertEqual(list(map(len, gaps)), self.framing["lengths"])
                self.assertEqual(sorted("".join(map("".join, gaps))), sorted(self.framing["payload"]))

    def test_only_24_row_tables_are_selected(self):
        tables = audit.load_edit_tables()
        self.assertEqual(set(tables), {"kedri/spelled/sequence", "kedri/spelled/lcs"})
        self.assertTrue(all(len(rows) == 24 for rows in tables.values()))

    def test_index_edges(self):
        self.assertEqual(audit.index_char("ABCDE", 1, 1, "start", "strict"), "A")
        self.assertEqual(audit.index_char("ABCDE", 1, 1, "end", "strict"), "E")
        self.assertEqual(audit.index_char("ABCDE", 5, 0, "start", "strict"), "X")
        self.assertEqual(audit.index_char("ABCDE", 5, 0, "start", "cyclic"), "A")

    def test_architect_feature_vectors_are_24_wide(self):
        vectors = audit.architect_feature_vectors(audit.load_edit_tables())
        self.assertTrue(vectors)
        self.assertTrue(all(len(vector) == 24 for vector in vectors.values()))

    def test_pearson_controls(self):
        self.assertAlmostEqual(audit.pearson([1, 2, 3], [2, 4, 6]), 1.0)
        self.assertAlmostEqual(audit.pearson([1, 2, 3], [6, 4, 2]), -1.0)


if __name__ == "__main__":
    unittest.main()
