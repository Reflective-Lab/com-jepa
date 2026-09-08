"""CPU-only Random Forest demonstration on explicitly fictional tabular snapshots.

Run: python -m com_jepa.forest_demo --output artifacts/forest-demo.json
This is a pipeline exercise, not a validated organisational predictor.
"""

import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from importlib.metadata import version
import json
import math
from pathlib import Path
import random

from .events import timestamp


FEATURES = ("days_remaining", "unresolved_dependencies", "evidence_age_days", "remaining_work_units")
TARGET = "all_criteria_met_by_version_deadline"
SETTLED = {"met": 1, "not_met": 0}
UNRESOLVED = {"unknown", "right_censored", "disputed"}
GENERATOR_VERSION = "toy-tabular-v1"
START = datetime(2025, 1, 1, tzinfo=timezone.utc)


def stamp(value):
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_rows(samples=300, seed=42):
    """Invent one snapshot per independent initiative, with a declared noisy rule.

    Numbers and causal-looking relationships are authored assumptions. This does
    not consume the event ledger or assign labels to the discussion cards.
    """
    if not 120 <= samples <= 2000:
        raise ValueError("samples must be between 120 and 2000 for this small demo")
    rng = random.Random(seed)
    rows = []
    for i in range(samples):
        as_of = START + timedelta(days=i)
        days, dependencies, age, work = rng.randint(2, 28), rng.randint(0, 4), rng.randint(0, 10), rng.randint(2, 30)
        logit = 1.2 + 0.13 * days - 0.75 * dependencies - 0.06 * age - 0.13 * work
        probability = 1 / (1 + math.exp(-logit))
        status = "met" if rng.random() < probability else "not_met"
        if rng.random() < 0.06:
            status = rng.choice(sorted(UNRESOLVED))
        due = as_of + timedelta(days=days)
        rows.append({
            "data_origin": "fictional", "generator_version": GENERATOR_VERSION,
            "organisation_id": "fictional-org", "initiative_id": f"initiative-{i:04d}",
            "commitment_id": f"commitment-{i:04d}", "commitment_version": 1,
            "target": TARGET, "as_of": stamp(as_of), "due_at": stamp(due),
            "features_available_at": stamp(as_of),
            "features": dict(zip(FEATURES, (days, dependencies, age, work))),
            "label_status": status,
            "label_available_at": stamp(due + timedelta(days=rng.randint(1, 5))),
        })
    return rows


def feature_matrix(rows):
    """Explicit allowlist: neither identities nor future outcome fields are inputs."""
    matrix = []
    for row in rows:
        if timestamp(row["features_available_at"]) > timestamp(row["as_of"]):
            raise ValueError("features were unavailable at prediction cutoff")
        if set(row["features"]) != set(FEATURES):
            raise ValueError("unexpected or missing feature; review the allowlist")
        values = [row["features"][name] for name in FEATURES]
        if any(isinstance(v, bool) or not isinstance(v, (float, int)) or not math.isfinite(v) or v < 0 for v in values):
            raise ValueError("features must be finite non-negative numbers")
        days = (timestamp(row["due_at"]) - timestamp(row["as_of"])).total_seconds() / 86400
        if days <= 0 or days != row["features"]["days_remaining"]:
            raise ValueError("days_remaining must match the future version deadline")
        matrix.append(values)
    return matrix


def temporal_split(rows, training_cutoff, test_start, evaluation_as_of):
    """One snapshot per initiative; train labels must have settled before fitting.

    This narrow contract deliberately rejects repeated initiatives rather than
    pretending to implement full trajectory/component grouping.
    """
    train_at, test_at, evaluate_at = map(timestamp, (training_cutoff, test_start, evaluation_as_of))
    if not train_at < test_at <= evaluate_at:
        raise ValueError("require training_cutoff < test_start <= evaluation_as_of")
    feature_matrix(rows)
    seen_initiatives, seen_commitments = set(), set()
    train, test, excluded = [], [], Counter()
    for row in rows:
        if row["data_origin"] != "fictional" or row["generator_version"] != GENERATOR_VERSION:
            raise ValueError("this demonstration accepts only its declared fictional row format")
        if row["target"] != TARGET or row["commitment_version"] != 1:
            raise ValueError("this demo supports only the original version and fixed target")
        initiative = row["organisation_id"], row["initiative_id"]
        commitment = row["organisation_id"], row["commitment_id"]
        if initiative in seen_initiatives or commitment in seen_commitments:
            raise ValueError("demo requires one unique initiative and commitment per row")
        seen_initiatives.add(initiative)
        seen_commitments.add(commitment)
        as_of, known = timestamp(row["as_of"]), timestamp(row["label_available_at"])
        if known < timestamp(row["due_at"]):
            raise ValueError("assessment availability cannot precede the deadline in this demo")
        status = row["label_status"]
        if status not in SETTLED and status not in UNRESOLVED:
            raise ValueError("unsupported label status")
        if as_of < train_at:
            if known > train_at:
                excluded["training_label_not_yet_available"] += 1
            elif status not in SETTLED:
                excluded[f"training_{status}"] += 1
            else:
                train.append(row)
        elif as_of < test_at:
            excluded["temporal_gap"] += 1
        elif as_of > evaluate_at or known > evaluate_at:
            excluded["test_not_yet_assessable"] += 1
        elif status not in SETTLED:
            excluded[f"test_{status}"] += 1
        else:
            test.append(row)
    order = lambda r: (r["as_of"], r["initiative_id"])
    return sorted(train, key=order), sorted(test, key=order), dict(sorted(excluded.items()))


def run_demo(samples=300, seed=42):
    # Optional dependency: the event-validation commands do not import sklearn.
    from sklearn.dummy import DummyClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, brier_score_loss, log_loss

    rows = generate_rows(samples, seed)
    training_cutoff = stamp(START + timedelta(days=int(samples * 0.6)))
    test_start = stamp(timestamp(training_cutoff) + timedelta(days=30))
    evaluation_as_of = stamp(START + timedelta(days=samples + 40))
    train, test, excluded = temporal_split(rows, training_cutoff, test_start, evaluation_as_of)
    x_train, x_test = feature_matrix(train), feature_matrix(test)
    y_train = [SETTLED[r["label_status"]] for r in train]
    y_test = [SETTLED[r["label_status"]] for r in test]
    if len(set(y_train)) != 2 or not y_test:
        raise ValueError("need both training classes and at least one settled test outcome")
    models = {
        "historical_base_rate": DummyClassifier(strategy="prior"),
        "random_forest": RandomForestClassifier(
            n_estimators=100, max_depth=6, min_samples_leaf=5, random_state=seed, n_jobs=1,
        ),
    }
    scores, probabilities = {}, {}
    for name, model in models.items():
        model.fit(x_train, y_train)
        positive_column = list(model.classes_).index(1)
        predicted = model.predict_proba(x_test)[:, positive_column]
        probabilities[name] = predicted.tolist()
        scores[name] = {
            "brier_score": float(brier_score_loss(y_test, predicted)),
            "log_loss": float(log_loss(y_test, predicted, labels=[0, 1])),
            "accuracy_at_0_5": float(accuracy_score(y_test, predicted >= 0.5)),
        }
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return {
        "purpose": "synthetic_pipeline_demonstration_not_organisational_evidence",
        "generator_version": GENERATOR_VERSION, "seed": seed,
        "target": TARGET, "positive_class": "met",
        "features": list(FEATURES), "dataset_sha256": sha256(payload.encode()).hexdigest(),
        "environment": {p: version(p) for p in ("scikit-learn", "numpy", "scipy")},
        "training_cutoff": training_cutoff, "test_start": test_start,
        "evaluation_as_of": evaluation_as_of,
        "counts": {"generated": len(rows), "train": len(train), "test": len(test), "excluded": excluded},
        "train_fulfilment_rate": sum(y_train) / len(y_train),
        "test_fulfilment_rate": sum(y_test) / len(y_test),
        "training_initiatives": [r["initiative_id"] for r in train],
        "forest_parameters": models["random_forest"].get_params(),
        "metrics": scores,
        "test_predictions": [
            {"initiative_id": row["initiative_id"], "as_of": row["as_of"],
             "label_available_at": row["label_available_at"], "observed_label": row["label_status"],
             "features": row["features"],
             **{name: values[i] for name, values in probabilities.items()}}
            for i, row in enumerate(test)
        ],
        "limitations": [
            "Labels follow an invented rule, not observations from organisations.",
            "One synthetic organisation; independent initiatives; no revisions, dependencies between rows, or interventions.",
            "Same generator in train and test; no real-world transfer or JEPA conclusions.",
            "Fixed forest; no tuning, calibration study, uncertainty intervals, or causal claims.",
            "Toy snapshots are not exports of the draft event ledger or the fictional challenge cards.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=300)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, help="optional JSON report; use ignored artifacts/")
    args = parser.parse_args()
    try:
        report = run_demo(args.samples, args.seed)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("x") as stream:
                json.dump(report, stream, indent=2, allow_nan=False)
                stream.write("\n")
    except ModuleNotFoundError:
        parser.exit(1, "Install the optional demo dependencies: python -m pip install -r requirements-ml.txt\n")
    except (ValueError, OSError) as error:
        parser.exit(1, f"error: {error}\n")
    print("SYNTHETIC PIPELINE DEMO — not evidence of organisational prediction quality")
    print(f"Rows: {report['counts']['generated']} generated; {report['counts']['train']} train; {report['counts']['test']} test")
    print(f"Train labels available by {report['training_cutoff']}; test snapshots from {report['test_start']}")
    print(f"Excluded: {json.dumps(report['counts']['excluded'], sort_keys=True)}")
    print("Model                     Brier (lower)  Log loss (lower)  Accuracy @ 0.5")
    for name, metrics in report["metrics"].items():
        print(f"{name:25} {metrics['brier_score']:.4f}         {metrics['log_loss']:.4f}            {metrics['accuracy_at_0_5']:.4f}")
    print("Random Forest probabilities are uncalibrated; no causal or transfer claim.")
    if args.output:
        print(f"Report: {args.output}")


if __name__ == "__main__":
    main()
