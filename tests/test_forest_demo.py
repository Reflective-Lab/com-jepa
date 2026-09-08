from copy import deepcopy
from importlib.util import find_spec
import math
import unittest

from com_jepa.forest_demo import FEATURES, feature_matrix, generate_rows, run_demo, temporal_split


class ForestDataBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.rows = generate_rows()
        self.cutoffs = ("2025-06-30T00:00:00Z", "2025-07-30T00:00:00Z", "2025-12-07T00:00:00Z")

    def test_future_labels_are_not_training_examples(self):
        self.rows[0]["label_available_at"] = "2025-07-01T00:00:00Z"
        train, test, excluded = temporal_split(self.rows, *self.cutoffs)
        self.assertNotIn(self.rows[0], train)
        self.assertGreater(excluded["training_label_not_yet_available"], 0)
        self.assertTrue(all(r["label_available_at"] <= self.cutoffs[0] for r in train))
        self.assertTrue(all(r["as_of"] >= self.cutoffs[1] for r in test))
        self.assertFalse({r["initiative_id"] for r in train} & {r["initiative_id"] for r in test})
        self.assertEqual(len(train) + len(test) + sum(excluded.values()), len(self.rows))

    def test_unknown_censored_disputed_are_not_failures(self):
        for status in ("unknown", "right_censored", "disputed"):
            with self.subTest(status=status):
                rows = deepcopy(self.rows)
                rows[0]["label_status"] = status
                train, _, excluded = temporal_split(rows, *self.cutoffs)
                self.assertNotIn(rows[0], train)
                self.assertGreater(excluded[f"training_{status}"], 0)

    def test_future_features_and_feature_label_leakage_are_rejected(self):
        row = deepcopy(self.rows[0])
        row["features_available_at"] = "2025-01-02T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "unavailable"):
            feature_matrix([row])
        row = deepcopy(self.rows[0])
        row["features"]["label_status"] = 1
        with self.assertRaisesRegex(ValueError, "allowlist"):
            feature_matrix([row])

    def test_outcomes_and_identifiers_do_not_change_feature_matrix(self):
        altered = deepcopy(self.rows)
        for row in altered:
            row["label_status"] = "unknown"
            row["initiative_id"] = "ignored-by-feature-builder"
        self.assertEqual(feature_matrix(self.rows), feature_matrix(altered))
        self.assertEqual(len(feature_matrix(self.rows)[0]), len(FEATURES))

    def test_repeated_initiatives_cannot_cross_the_split(self):
        self.rows[-1]["initiative_id"] = self.rows[0]["initiative_id"]
        with self.assertRaisesRegex(ValueError, "unique initiative"):
            temporal_split(self.rows, *self.cutoffs)

    def test_test_labels_after_evaluation_cutoff_are_excluded(self):
        self.rows[-1]["label_available_at"] = "2026-01-01T00:00:00Z"
        _, test, excluded = temporal_split(self.rows, *self.cutoffs)
        self.assertNotIn(self.rows[-1], test)
        self.assertGreater(excluded["test_not_yet_assessable"], 0)

    def test_nonfinite_features_and_inconsistent_deadlines_are_rejected(self):
        for value in (math.nan, math.inf, -1):
            with self.subTest(value=value):
                row = deepcopy(self.rows[0])
                row["features"]["evidence_age_days"] = value
                with self.assertRaises(ValueError):
                    feature_matrix([row])
        self.rows[0]["features"]["days_remaining"] += 1
        with self.assertRaisesRegex(ValueError, "deadline"):
            feature_matrix(self.rows)


@unittest.skipUnless(find_spec("sklearn"), "optional ML demo: install requirements-ml.txt")
class ForestExecutionTests(unittest.TestCase):
    def test_reproducible_finite_predictions_and_training_only_base_rate(self):
        first, second = run_demo(), run_demo()
        self.assertEqual(first, second)
        self.assertIn("synthetic_pipeline", first["purpose"])
        for row in first["test_predictions"]:
            self.assertAlmostEqual(row["historical_base_rate"], first["train_fulfilment_rate"])
            self.assertTrue(0 <= row["random_forest"] <= 1)
        for scores in first["metrics"].values():
            self.assertTrue(all(math.isfinite(v) for v in scores.values()))
        # No assertion that the forest must win: that would canonise the generator.


if __name__ == "__main__":
    unittest.main()
