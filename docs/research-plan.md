# Research plan

Status: research proposal, 2026-09-08. Release 0.1.0 implements the draft event validator, a synthetic Random Forest baseline, and a [TabPFN-3 comparison with recorded GPU results](tabpfn-comparison.md). These exercise the pipeline on invented data; they do not satisfy the measurement or real-data evaluation gates below. No empirical organisational results yet.

## Primary question and target

Does an explicit history of commitments improve prediction and decision quality beyond the information already available in ordinary work records?

The first task predicts the probability that an accepted commitment **version** meets **all** of its stated acceptance criteria by that version's deadline, using only information available at a declared cutoff. Initially select a narrow family of commitments whose criteria can be independently assessed. Report original and revised versions separately; pre-register one primary scoring target per trajectory to avoid counting revisions as independent successes.

The outcome is not the next event in a log. It is externally supported fulfilment. Revisions, withdrawals, partial fulfilment, and disputed outcomes need their own treatment. Unknown and right-censored cases are not negative labels. A later survival-analysis task can use properly specified censoring and competing events.

## Hypotheses that can fail

| Hypothesis | Comparison | Evidence against it |
| --- | --- | --- |
| H1: commitment context adds value | Work-record features versus the same features plus commitment history | No reliable gain outside training initiatives, or capture cost exceeds benefit |
| H2: trajectories add value | Tabular summaries versus temporal/dependency models with access to the same raw history | No robust gain across time splits and seeds |
| H3: the JEPA objective adds value | JEPA versus supervised and masked-event objectives with comparable encoders, information, and tuning budgets | Gains disappear under fair controls, or are too expensive |
| H4: useful structure transfers | Local-only, shared zero-shot, and shared-plus-local models on held-out organisations | Negative transfer or no benefit after local calibration |
| H5: model assistance improves practice | A prospective comparison of decision processes with and without advice | Better prediction without better outcomes, or reduced human understanding |

Choose primary metrics, meaningful effect sizes, uncertainty estimates, and go/no-go criteria with pilot partners **before** inspecting test results. There is no universal minimum dataset size for JEPA; count independent trajectories, settled outcomes, event diversity, and organisations, then inspect learning curves.

## Experiments in order

### 0. Measurement feasibility

Start with one recurring commitment family and a small discovery group, for example three to five partner organisations if available. This is for contract design and feasibility, not a representative sample of organisations.

Measure missing fields, outcome-observation delay, disagreement between assessors, revision frequency, and collection burden. Include successful, failed, revised, cancelled, and unresolved cases. Reconstruct historical availability conservatively; do not invent timestamps to make old data appear prospective. If independent assessors cannot agree on what “met” means, fix the target before fitting a model.

### 1. Conventional prediction

Pre-register base-rate and explicit-rule comparators. Then fit regularised logistic regression and gradient-boosted trees to as-of features: time remaining, declared scope, evidence freshness, unresolved dependencies, revision history, and action-stage counts. Restrict features to information reliably collected across the comparison groups. Compare to human forecasts collected before model advice when feasible.

Use prior outcomes available at the training cutoff. Fit imputers, encoders, normalisers, calibration, and feature selection on training/validation data only. Learn grouped rates with shrinkage or minimum-support rules; do not manufacture precision from a few examples. With insufficient settled data, report uncertainty and defer fitted models.

### 2. Temporal and dependency models

Test whether order, elapsed time, and dependencies matter beyond strong tabular summaries. Compare supervised sequence models and masked-event pretraining. An LLM-based forecaster is another useful comparator if it receives the same permitted history and its prompts, retrieval, model version, and budget are recorded. LLMs can also assist extraction; extracted facts require provenance and review before becoming accepted organisational records.

Predictive process monitoring is an established neighbouring field, not something com-jepa invents. Its benchmarks offer methodological starting points, but ordinary event logs may lack commitment authority, revision semantics, and beneficiary acceptance. See [Teinemaa et al.](https://arxiv.org/abs/1707.06766).

### 3. Candidate commitment JEPA

Proposed context: a typed, time-aware sequence or subgraph of commitments, observations, dependencies, and actions known at time *t*. Proposed target: a representation of a subsequent window. Semantic target windows must be chosen experimentally; arbitrary masking can teach record reconstruction without learning useful organisational dynamics.

An online encoder represents context. A predictor estimates a target representation produced by a stop-gradient target encoder, potentially updated by exponential moving average. The loss encourages agreement in representation space. Monitor collapse, variance, and sensitivity to meaningful changes. This is an architecture proposal, not implemented code here.

For future prediction, only context available at *t* may reach the predictor. Future observations belong on the target side during training. A separate action-conditioned experiment may include a proposed action already specified at *t*; it must not condition on an action whose eventual execution was unknown then. Self-supervised pretraining still requires strict dataset splits.

Freeze or fine-tune the representation under predeclared protocols and fit outcome heads. Test calibration, label efficiency, robustness, and compute cost. Latent distance is not a probability of failure. Do not call an action-conditioned forecast a causal estimate.

Use same-information comparisons and encoder/objective ablations. A richer JEPA input against impoverished tabular inputs tests information access, not the JEPA objective. Record parameter counts, data access, tuning trials, seeds, runtime, and hardware. The relevant precedents are [I-JEPA](https://arxiv.org/abs/2301.08243), [T-JEPA](https://arxiv.org/abs/2410.05016), and [V-JEPA 2](https://arxiv.org/abs/2506.09985); organisational validity and efficiency remain open.

### 4. Transfer and local learning

Hold out entire organisations. A zero-shot test organisation must not contribute even unlabelled pretraining data. Study local adaptation separately with a declared quantity of local history and a later untouched test period. Compare shared-only, local-only, and shared-plus-local alternatives by sector, size, commitment family, and observation quality when sample size permits.

Common action names do not establish common causal mechanisms. Differences in authority, resources, culture, and measurement can make shared representations misleading. Include out-of-distribution detection or explicit abstention and test forgetting after adaptation. Private or federated training is a later engineering choice, not a guarantee of privacy or transfer.

### 5. From prediction to improved commitments

Start with shadow forecasts hidden from decision-makers. Then run a prospective advice study with a predeclared comparison and sufficient independent groups. Randomisation or a carefully justified alternative is needed for causal claims; dependencies between commitments can create spillovers across groups.

Log what advice was shown, when, to whom by role, whether it was challenged, and what intervention followed. Predictions can change the outcomes they predict: see [Performative Prediction](https://proceedings.mlr.press/v119/perdomo20a.html). A risk correctly averted is different from an unhelpful false alarm.

Measure beneficiary outcomes, revision costs, time to recognise drift, decision effort, and human ability to explain and challenge the decision. Preserve dissent and include harmful or burdensome effects in the report. “More commitments completed” alone is vulnerable to choosing easier promises or weakening acceptance criteria.

## Evaluation rules

- Split forward in time and group whole initiatives or connected dependency components to limit correlated leakage. Purge overlapping windows around boundaries. Report the unit of analysis and effective sample size; windows are not independent organisations.
- Freeze a test set and do model selection on separate validation data. Use only labels settled by each historical training cutoff. Record observation coverage and exclusions, not just scored cases.
- For binary fulfilment, report Brier score, log loss, calibration, and class prevalence; add precision–recall measures for rare failures. Use grouped uncertainty intervals. Set decision thresholds on validation data using an agreed intervention cost model.
- Report performance by horizon and cohort, abstention coverage, drift, collection burden, and inference/training cost. A narrow confidence interval from many correlated windows is not evidence of broad transfer.
- Version the dataset, feature builder, split, encoder, model, calibration, and evaluation code. Publish limitations and negative results. Public data must have separate rights and disclosure review.

## Continuous learning does not mean continuous deployment

Collect events continuously. Train candidate updates periodically when enough settled evidence exists. Promote only after regression, calibration, drift, and governance review; retain rollback. Freeze the model version within a decision episode. Model weights are derived artefacts, not the organisation's memory or its authority to commit.

Stop or narrow the study if labels cannot be trusted, predictive improvements do not survive fair comparisons, recording becomes surveillance, or assistance undermines human agency. There is no requirement to reach JEPA for the project to succeed.
