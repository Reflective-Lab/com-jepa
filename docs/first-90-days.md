# First 90 days

This is a proposed sequence, not a promise of a trained model within a quarter. Advancement depends on evidence and partner availability.

| Period | Work | Reviewable output | Gate |
| --- | --- | --- | --- |
| Weeks 1–2 | Critique the thesis, choose one commitment family, recruit a small discovery group | Research questions, fictional trajectories, target definition | Practitioners agree the target matters and can be assessed |
| Weeks 3–6 | Map two work surfaces into commitment history; run a prospective collection pilot | Adapter specification, data card, capture-burden and missingness report | History and outcomes can be collected without relying on retrospective invention |
| Weeks 7–10 | Inspect label reliability and build the first as-of dataset | Versioned dataset manifest, adjudication policy, frozen split and baseline protocol | Enough independent settled outcomes for a defensible first analysis |
| Weeks 11–13 | Evaluate base rates and, if justified, conventional ML; review human workflow | Baseline report or explicit “insufficient data” finding | Decide whether to expand data collection, study advice, or stop |

Sequence/graph models and JEPA follow only if these results justify them. Long commitment horizons may mean the first quarter produces measurement evidence rather than trained models. That is an acceptable outcome.

## Initial work packages

The [fictional challenge set](../examples/challenge-set/README.md) and [partner discovery guide](partner-discovery.md) provide starting material for the first two work packages. Gather participants' own accounts before showing the cards; no case constitutes a partner finding or a training label.

1. **Target definition:** choose a recurring promise, specify fulfilment and observation, and identify where revisions make labels ambiguous.
2. **Contract review:** challenge the action vocabulary, version lineage, beneficiary role, late evidence, and missing-data semantics with fictional counterexamples.
3. **Measurement adapter:** export one prospective trajectory across two surfaces, preserving authority and provenance.
4. **Benchmark design:** implement label adjudication, grouped time splits, base rates, logistic regression, and gradient-boosted trees in that order of complexity.
5. **Human learning:** define a separate evaluation of understanding, challenge, and transfer; avoid using recall scores as organisational success labels.
6. **JEPA design note:** specify context/target masking, encoder parity, collapse checks, outcome heads, and compute-budget controls before training.

Each can begin with a public issue containing the question, a concrete example, an expected artefact, and a criterion that could disprove the proposed approach. Do not put partner data into those issues.

## A Birds of a Feather session

**Working title:** Can organisations learn from the commitments they make?

**Invitation:** We are starting an open research project on organisational commitment trajectories: what was promised, what was known, what action followed, and what happened. We want to test simple predictive models first and ask whether JEPA-style representations could eventually improve learning across organisations. Bring experience in operational decisions, process mining, applied ML, representation learning, or human–AI collaboration. No JEPA expertise is required.

**A 45-minute structure:**

- 5 minutes: the organisation-first thesis and one fictional commitment.
- 10 minutes: define its outcome, revision, and evidence gaps together.
- 10 minutes: identify the smallest useful dataset and strongest simple baseline.
- 10 minutes: discuss what would justify a temporal model or JEPA, and what would invalidate the idea.
- 10 minutes: agree on two or three bounded follow-up artefacts and willing contributors.

**Questions worth leaving unresolved:** What cannot be expressed as a commitment without losing meaning? Which outcomes are independent of internal status reporting? Where do action types transfer between organisations? How can advice strengthen human judgment? What result would make us keep the simple model?

This is a credible session to convene as the project initiator. The role is to make the problem precise and invite informed criticism. Training an LLM is neither a prerequisite for participation nor the central skill required for the first phase.
