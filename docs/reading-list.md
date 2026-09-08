# Reading list and claims ledger

The project draws on organisational design, predictive process monitoring, representation learning, and human–AI collaboration. It does not claim that commitment-oriented work or outcome prediction is new. Links were reviewed while bootstrapping the project on 2026-09-08; this is a starting bibliography, not a systematic review.

## Reflective's argument

| Source | Contribution here | Status |
| --- | --- | --- |
| [The Physics of Organizations](https://www.reflective.se/series/physics), especially [The Commitment Machine](https://www.reflective.se/signals/the-commitment-machine) | Commitments as durable coordination across people and time | Author's organisational design thesis |
| [Organizational Capability](https://www.reflective.se/series/organizational-capability), especially [Human Judgment](https://www.reflective.se/signals/human-judgment) | Reasoning, authority, drift, and learning from prior decisions | Design argument and proposed operating model |
| [The System 3 Age](https://www.reflective.se/series/system-3), especially [System 3 Should Grow System 2](https://www.reflective.se/signals/system-3-should-grow-system-2) | AI assistance should develop human capacity and preserve deliberation | Design objective; effects need independent evaluation |
| [The Acceptance Paradox](https://www.reflective.se/signals/the-acceptance-paradox) | Engage people in shaping intent and make outputs interrogable | Practical design proposal |
| [Reflective research directory](https://www.reflective.se/labs/research), especially [the JEPA report](https://www.reflective.se/labs/research/jepa) | Earlier formulation of learning from initiative trajectories and reasons to delay training | Technical background; implementation claims are separate from research hypotheses |

## Primary technical starting points

- **Assran et al., I-JEPA (2023).** [Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture](https://arxiv.org/abs/2301.08243). Predicting target representations from context is the architectural precedent. Image results do not establish organisational applicability.
- **Thimonier et al., T-JEPA (ICLR 2025).** [Augmentation-Free Self-Supervised Learning for Tabular Data](https://arxiv.org/abs/2410.05016). A relevant structured-data method that predicts representations of feature subsets within a sample. It does not demonstrate longitudinal organisational dynamics or cross-organisation transfer.
- **Assran et al., V-JEPA 2 (2025).** [Self-Supervised Video Models Enable Understanding, Prediction and Planning](https://arxiv.org/abs/2506.09985). A precedent for predictive representations and subsequent action-conditioned training in physical settings. Reusing its weights for organisational events is not an established path; we are borrowing research ideas, not assuming modality transfer.
- **Teinemaa et al. (2018 revision).** [Outcome-Oriented Predictive Process Monitoring: Review and Benchmark](https://arxiv.org/abs/1707.06766). Establishes important neighbouring work and the need for comparable evaluation across event-log prediction methods.
- **Perdomo et al. (ICML 2020).** [Performative Prediction](https://proceedings.mlr.press/v119/perdomo20a.html). A foundation for treating predictions as potential influences on the outcomes they forecast.

Further lineage to examine includes language/action approaches to cooperative work, coordination theory, organisational learning, survival analysis, and causal inference. Contributions should add primary sources with a short account of exactly which claim they support.

## Claim boundaries

| We can say now | We cannot say yet |
| --- | --- |
| An explicit commitment history is a testable proposed learning substrate | It is universally the best organisational abstraction |
| JEPA has relevant precedents in other data modalities | It will outperform conventional ML on commitments |
| Shared representations and local adaptation are research questions | One trained model is valid for most organisations |
| Durable context can support deliberation by design | The design has been shown to prevent cognitive surrender |
| Better forecasts may help people choose interventions | Observational action-conditioned forecasts identify causal effects |
| The schema, fictional replay, and synthetic Random Forest demo are executable | A real organisational dataset, validated organisational model, or deployed integration exists here |
