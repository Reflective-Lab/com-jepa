# A small Random Forest example

Status: executable synthetic pipeline demonstration. It trains a real Random Forest on invented tabular rows; it does not train an organisationally validated predictor, JEPA, or a foundation model.

## Run it locally

Use Python 3.14 for the pinned ML environment exercised in CI. From the repository root:

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements-ml.txt
.venv/bin/python -m com_jepa.forest_demo
.venv/bin/python -m com_jepa.forest_demo --output artifacts/forest-demo.json
.venv/bin/python -m unittest discover -s tests -v
```

The output option writes a JSON report and refuses to overwrite an existing file; choose a new filename for another experiment. `artifacts/` is ignored by Git. Without that option the model fits in memory, prints a comparison, and exits without saving data or model weights. It needs no GPU, API key, model download, or hosted service. Installing dependencies requires network access once.

The original `requirements.txt` remains sufficient for the event validator. Tests of the ML fit skip when scikit-learn is absent; the dedicated ML CI job installs it and runs the full suite.

## What the forest learns

The question is whether one accepted version meets all its criteria by its deadline. The demo invents 300 rows, each a different commitment in a different initiative within one fictional organisation. One row represents the information available at one prediction cutoff. All commitments are version 1; there are no revisions, shared resources, or interventions in this simplified simulation.

Four declared features are available at the cutoff:

| Feature | Invented range | Interpretation for the exercise |
| --- | --- | --- |
| `days_remaining` | 2–28 | Days from the prediction cutoff to the original deadline |
| `unresolved_dependencies` | 0–4 | Count of dependencies believed unresolved at that cutoff |
| `evidence_age_days` | 0–10 | Age of the latest relevant evidence |
| `remaining_work_units` | 2–30 | An invented measure of work remaining, with no cross-organisation meaning |

These are proposed teaching features, not a ratified extension of the event schema. The generator supplies their values directly. This code is **not** a feature extractor from real event histories. A real adapter must establish the units, provenance, and as-of derivation before reusing a feature name.

The entire invented probability rule is:

```text
z = 1.2 + 0.13 × days_remaining
        − 0.75 × unresolved_dependencies
        − 0.06 × evidence_age_days
        − 0.13 × remaining_work_units
p(met) = 1 / (1 + exp(−z))
```

Outcomes are Bernoulli draws from that probability; about 6% are independently marked unknown, right-censored, or disputed. This artificial missingness is much simpler than real observation processes. Labels become available one to five days after the deadline. Coefficients, feature ranges, independence, noise, missingness, and timing are all authored assumptions. They are not organisational findings or causal estimates.

The forest receives the four features and settled training labels. It does not receive the rule's probability, identities, future observations, or test labels. The same generator produces train and test rows, so a successful result demonstrates learning that artificial relationship. It cannot establish transfer outside the generator.

## Fit and compare

[RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) combines predictions from decision trees fitted to resampled training data. Here it uses 100 trees, maximum depth 6, minimum leaf size 5, one CPU worker, and a fixed random seed. The forest's probabilities are estimates from its tree ensemble; they are not automatically calibrated.

The comparator is [DummyClassifier with `strategy="prior"`](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html). It predicts the observed training fulfilment rate for every test row. This establishes whether the forest offers anything beyond that simple historical expectation under the toy generator.

The fit cutoff occurs 60% of the way through the generated daily prediction cutoffs. Only earlier rows whose labels are settled and available by that fit date can train either model. Test cutoffs begin 30 days later. Test labels must be available by the separately declared evaluation date. The report accounts for excluded rows by reason. There is no random train/test shuffle, hyperparameter search, or test-driven model selection.

There is one row per initiative and commitment. Repeated IDs are rejected, so the toy cannot silently put snapshots of the same initiative on both sides of the split. Real data needs a proper grouped temporal split and dependency-component handling; this restriction is not a general implementation of either.

## Read the output

The terminal prints both models' Brier score, log loss, and accuracy at a fixed 0.5 threshold. Lower Brier score and log loss are better; accuracy uses an arbitrary teaching threshold, not an agreed business cost. The JSON report records generation seed/version, dataset hash, split dates, exclusions, training prevalence, model parameters, library versions, and every scored test prediction.

No test requires the forest to beat the base rate. That would turn the generator's design into a success condition for the research. There are no confidence intervals, calibration experiment, fairness assessment, or causal claims here. Changing the seed demonstrates sampling variation, not robustness across organisations. Keep reported scores labelled **synthetic pipeline results**.

## Why this does not pre-empt partner discovery

The generator answers one engineering question: can we fit, evaluate, and inspect a conventional probability model while enforcing the selected temporal boundaries? It does not resolve the ambiguous challenge scenarios, assign labels to them, or enlarge them into a supposed organisational training corpus.

Partners can still reject these features, their units, the binary target, or the commitment abstraction. Any real dataset should follow the [data contract and stewardship work](data-contract.md) and the [research evaluation plan](research-plan.md), including independent assessment and grouped time splits. Passing this demo does not satisfy those gates.

## Where tabular foundation models fit

The structured-data models raised in discussion are useful comparison candidates. Our immediate task is table-based classification; forecasting a regular numerical time series is a different task unless we first define a justified transformation.

- [Google TabFM](https://research.google/blog/introducing-tabfm-a-zero-shot-foundation-model-for-tabular-data/) describes in-context tabular classification/regression using labelled examples without per-task weight updates. Google reports pretraining on diverse synthetic datasets and evaluation on real tabular benchmarks. That does not validate our much narrower invented organisational rule.
- [Prior Labs' TabPFN-3 documentation](https://docs.priorlabs.ai/changelog/tabpfn-3) describes tabular inference and local weights subject to licence acceptance. It is a possible later comparator; no weights, licence acceptance, API integration, or performance claim are included here.
- [Amazon Chronos-2](https://www.amazon.science/blog/introducing-chronos-2-from-univariate-to-universal-forecasting) concerns time-series forecasting with covariates. Its fit would require a separate time-series target; it is not a drop-in replacement for the classifier demonstrated here.

For a future comparison, give every model the same eligible historical labels and as-of features. In-context learning still uses task examples; “zero-shot” does not mean we can omit target definition or reveal future labels. Declare whether test rows are processed jointly, and prevent later test-row information from entering earlier forecasts through a shared context. Compare calibration, latency, data movement, licence/access terms, and cost alongside prediction quality.

PyTorch is not needed for this Random Forest. Add it when an actual neural-model experiment requires it. A tabular foundation model could become a strong baseline for com-jepa, but its availability does not establish that it should always be the default or that JEPA will be better.
