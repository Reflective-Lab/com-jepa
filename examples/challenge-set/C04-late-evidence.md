# C04 — Late evidence changes the assessment

Wholly fictional discussion case. No canonical outcome label.

## At the decision point

A storage service commits to keeping a shipment within an agreed temperature range through Friday at 17:00. Its acceptance criteria identify the monitoring interval and the measurement source.

At Thursday noon, all readings available to the prediction system are within range. A sensor has recorded additional readings locally, but those readings have not been transmitted. There is no basis at that cutoff to assert what Friday's measurements will show.

**Before revealing the outcome:** Which clocks must be preserved so a future training run can reproduce Thursday's information?

<details>
<summary>Reveal the later account</summary>

Friday at 17:20, the monitoring service reports a breach during the agreed interval. An assessor records `not_met` with that evidence. On Tuesday, a reviewed correction shows the transmitted series used an incorrect conversion. The corrected source readings support a later `met` assessment against the same original criteria. The original report and both assessments remain in the history.

The corrected readings concern Friday, but their corrected interpretation was first available Tuesday. Moving that knowledge back to Friday would change what the earlier predictor could have known.

</details>

## Questions for the participant

- What evidence permits the second assessment to supersede the first?
- What label would a training run on Monday have had access to? What changes for a later run?
- Would repeated evidence corrections reveal a delivery problem, a measurement problem, or both?

<details>
<summary>Maintainer discussion — provisional, not an answer key</summary>

The draft's occurrence and availability timestamps support late evidence; the context utility excludes it before availability. The draft also allows multiple assessments of one version. It has no typed correction link, adjudication rule, or label-selection implementation.

Selecting the last event by timestamp is not a sufficient governance rule. A later assertion can also be wrong or unauthorised. Preserve assessment provenance and distinguish a historical replay using labels then available from an evaluation using subsequently adjudicated outcomes. Both can be useful, but must be declared separately.

Candidate evidence includes the correction's basis, authorised adjudication, and immutable dataset manifests. This story does not establish that any real measurement source has those properties.

</details>
