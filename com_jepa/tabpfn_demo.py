"""Optional TabPFN-3 GPU comparison using the forest demo's exact synthetic split.

Requires a separately downloaded, hash-verified checkpoint. Does not serve a model.
"""

import argparse
from datetime import datetime, timezone
from hashlib import file_digest
from importlib.metadata import version
import json
from pathlib import Path
import platform
from time import perf_counter

from .forest_demo import SETTLED, feature_matrix, generate_rows, run_demo, temporal_split


MODEL_REPO = "Prior-Labs/tabpfn_3"
MODEL_REVISION = "24a16a89d245878b846555110985634aa2e656d7"
MODEL_FILENAME = "tabpfn-v3-classifier-v3_default.ckpt"
MODEL_SHA256 = "d0d865d54dfbc524f5703104be90620182dca7e5fb2c16de72e9959ea18f3988"
MODEL_LICENCE = "https://huggingface.co/Prior-Labs/tabpfn_3/blob/" + MODEL_REVISION + "/LICENSE"


def verify_checkpoint(path, expected_sha256):
    if len(expected_sha256) != 64 or any(c not in "0123456789abcdef" for c in expected_sha256):
        raise ValueError("checkpoint SHA-256 must be 64 lowercase hexadecimal characters")
    with Path(path).open("rb") as stream:
        actual = file_digest(stream, "sha256").hexdigest()
    if actual != expected_sha256:
        raise ValueError("checkpoint hash mismatch; refusing to load model")
    return actual


def predict_independently(estimator, rows):
    """A future test row must not enter an earlier row's preprocessing/context."""
    import numpy as np

    classes = list(estimator.classes_)
    if set(classes) != {0, 1}:
        raise ValueError("expected classes 0=not_met and 1=met")
    positive_column = classes.index(1)
    predictions = []
    for row in rows:
        output = np.asarray(estimator.predict_proba(np.asarray([row], dtype=float)))
        if output.shape != (1, 2) or not np.isfinite(output).all():
            raise ValueError("invalid probability response")
        if (output < 0).any() or (output > 1).any() or not np.allclose(output.sum(axis=1), 1):
            raise ValueError("invalid probability distribution")
        predictions.append(float(output[0, positive_column]))
    return np.asarray(predictions)


def comparison(checkpoint, expected_sha256, samples=300, seed=42, gpu_memory_gib=4):
    checkpoint = Path(checkpoint).resolve()
    if expected_sha256 != MODEL_SHA256:
        raise ValueError("this adapter pins one checkpoint; update its provenance before changing weights")
    checkpoint_hash = verify_checkpoint(checkpoint, expected_sha256)
    if checkpoint.name != MODEL_FILENAME:
        raise ValueError("use the explicitly documented TabPFN-3 checkpoint filename")
    if not 0 < gpu_memory_gib <= 8:
        raise ValueError("GPU allocation budget must be greater than 0 and at most 8 GiB")

    import torch
    from sklearn.metrics import accuracy_score, brier_score_loss, log_loss
    from tabpfn import TabPFNClassifier

    if not torch.cuda.is_available():
        raise ValueError("this experiment requires a working CUDA GPU; no silent CPU fallback")
    properties = torch.cuda.get_device_properties(0)
    budget_bytes = int(gpu_memory_gib * 1024**3)
    torch.cuda.set_per_process_memory_fraction(min(1.0, budget_bytes / properties.total_memory), 0)
    torch.set_num_threads(2)
    torch.manual_seed(seed)
    torch.cuda.reset_peak_memory_stats(0)

    baseline_start = perf_counter()
    report = run_demo(samples, seed)
    baseline_seconds = perf_counter() - baseline_start
    rows = generate_rows(samples, seed)
    train, test, excluded = temporal_split(rows, report["training_cutoff"], report["test_start"], report["evaluation_as_of"])
    if [r["initiative_id"] for r in train] != report["training_initiatives"]:
        raise ValueError("training split differs from baseline")
    if [r["initiative_id"] for r in test] != [r["initiative_id"] for r in report["test_predictions"]]:
        raise ValueError("test split differs from baseline")
    if excluded != report["counts"]["excluded"]:
        raise ValueError("exclusion policy differs from baseline")

    import numpy as np

    x_train, x_test = feature_matrix(train), feature_matrix(test)
    y_train = np.asarray([SETTLED[r["label_status"]] for r in train])
    y_test = np.asarray([SETTLED[r["label_status"]] for r in test])
    estimator = TabPFNClassifier(
        model_path=checkpoint, device="cuda", random_state=seed,
        n_estimators=4, n_preprocessing_jobs=1,
        fit_mode="fit_preprocessors", softmax_temperature=0.9,
    )
    torch.cuda.synchronize()
    start = perf_counter()
    estimator.fit(np.asarray(x_train, dtype=float), y_train)
    torch.cuda.synchronize()
    fit_seconds = perf_counter() - start
    start = perf_counter()
    predicted = predict_independently(estimator, x_test)
    torch.cuda.synchronize()
    predict_seconds = perf_counter() - start
    report["metrics"]["tabpfn_3"] = {
        "brier_score": float(brier_score_loss(y_test, predicted)),
        "log_loss": float(log_loss(y_test, predicted, labels=[0, 1])),
        "accuracy_at_0_5": float(accuracy_score(y_test, predicted >= 0.5)),
    }
    for row, probability in zip(report["test_predictions"], predicted):
        row["tabpfn_3"] = float(probability)
    report["environment"].update({p: version(p) for p in ("tabpfn", "torch", "huggingface-hub")})
    report["environment"].update({"python": platform.python_version(), "architecture": platform.machine(),
                                   "gpu": properties.name, "cuda_runtime": torch.version.cuda})
    report["candidate"] = {
        "name": "TabPFN-3", "repository": MODEL_REPO, "revision": MODEL_REVISION,
        "filename": checkpoint.name, "sha256": checkpoint_hash, "licence": MODEL_LICENCE,
        "n_estimators": 4, "random_state": seed, "device": "cuda", "n_preprocessing_jobs": 1,
        "resolved_n_estimators": int(estimator.n_estimators_),
        "fit_mode": "fit_preprocessors", "softmax_temperature": 0.9,
        "prediction_protocol": "one_test_row_per_call_with_fixed_training_context",
        "gpu_allocator_budget_gib": gpu_memory_gib,
        "peak_torch_allocated_bytes": torch.cuda.max_memory_allocated(0),
        "peak_torch_reserved_bytes": torch.cuda.max_memory_reserved(0),
    }
    report["timing_seconds"] = {
        "complete_baseline_demo": baseline_seconds,
        "tabpfn_fit_including_model_loading": fit_seconds,
        "tabpfn_predict_all_test_rows_individually": predict_seconds,
    }
    report["implementation_sha256"] = {}
    report["evaluated_at_utc"] = datetime.now(timezone.utc).isoformat()
    for name in ("forest_demo.py", "tabpfn_demo.py"):
        with Path(__file__).with_name(name).open("rb") as stream:
            report["implementation_sha256"][name] = file_digest(stream, "sha256").hexdigest()
    report["limitations"].extend([
        "One pretrained checkpoint, one synthetic generator and seed; no claim of model superiority or organisational validity.",
        "TabPFN has external pretraining; this comparison does not isolate architecture from pretraining.",
        "GPU timing is from a shared machine and single-row prediction; not a controlled hardware speed benchmark.",
        "CUDA seeds do not guarantee bitwise reproducibility across platforms or library versions.",
        "Allocator budget is not a hard bound on all process or unified-memory use.",
        "TabPFN-3 weights and outputs have their own non-commercial licence; the repository MIT licence does not replace it.",
    ])
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--checkpoint-sha256", default=MODEL_SHA256)
    parser.add_argument("--samples", type=int, default=300)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--gpu-memory-gib", type=float, default=4)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError("output already exists; choose a new report filename")
        report = comparison(args.checkpoint, args.checkpoint_sha256, args.samples, args.seed, args.gpu_memory_gib)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x") as stream:
            json.dump(report, stream, indent=2, allow_nan=False)
            stream.write("\n")
    except ModuleNotFoundError as error:
        parser.exit(1, f"Missing optional dependency: {error.name}. See docs/tabpfn-comparison.md.\n")
    except (ValueError, OSError) as error:
        parser.exit(1, f"error: {error}\n")
    print("SYNTHETIC GPU COMPARISON — not evidence of organisational prediction quality")
    print(f"Train: {report['counts']['train']}; test: {report['counts']['test']}; generator seed: {report['seed']}")
    print("Model                     Brier (lower)  Log loss (lower)  Accuracy @ 0.5")
    for name, metrics in report["metrics"].items():
        print(f"{name:25} {metrics['brier_score']:.4f}         {metrics['log_loss']:.4f}            {metrics['accuracy_at_0_5']:.4f}")
    print(f"TabPFN-3: checkpoint {report['candidate']['sha256']}")
    print(f"Report: {args.output}")


if __name__ == "__main__":
    main()
