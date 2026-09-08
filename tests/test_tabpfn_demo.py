from hashlib import sha256
from importlib.util import find_spec
from pathlib import Path
import tempfile
import unittest

from com_jepa.tabpfn_demo import predict_independently, verify_checkpoint


class CheckpointTests(unittest.TestCase):
    def test_changed_checkpoint_is_rejected_before_loading(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.ckpt"
            path.write_bytes(b"fictional checkpoint for hash test")
            expected = sha256(path.read_bytes()).hexdigest()
            self.assertEqual(verify_checkpoint(path, expected), expected)
            path.write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                verify_checkpoint(path, expected)
            with self.assertRaisesRegex(ValueError, "64 lowercase"):
                verify_checkpoint(path, "invalid")


@unittest.skipUnless(find_spec("numpy"), "optional ML adapter tests: install requirements-ml.txt")
class PredictionIsolationTests(unittest.TestCase):
    def test_each_call_sees_one_row_and_positive_class_is_looked_up(self):
        class Estimator:
            classes_ = [1, 0]

            def __init__(self):
                self.seen = []

            def predict_proba(self, rows):
                self.seen.append(rows.tolist())
                return [[float(rows[0][0]), 1 - float(rows[0][0])]]

        estimator = Estimator()
        self.assertEqual(predict_independently(estimator, [[0.2], [0.8]]).tolist(), [0.2, 0.8])
        self.assertEqual(estimator.seen, [[[0.2]], [[0.8]]])

    def test_invalid_probabilities_fail_instead_of_becoming_metrics(self):
        class Estimator:
            classes_ = [0, 1]

            def predict_proba(self, rows):
                return [[0.4, 0.8]]

        with self.assertRaisesRegex(ValueError, "distribution"):
            predict_independently(Estimator(), [[0.2]])


if __name__ == "__main__":
    unittest.main()
