# A fictional commitment trajectory

Every entity, event, source, and probability in `fictional-trajectory.jsonl` is invented. This is an executable specification example, not a training dataset or benchmark. No model generated the example's probability.

For cases that challenge the contract and its scope, see the [fictional challenge set](challenge-set/README.md). Those discussion cards include unresolved semantics and are not JSONL fixtures. Start partner conversations with the [discovery guide](../docs/partner-discovery.md).

The fictional team promises an integration by Friday 9 January. It later agrees a Monday 12 January deadline with the customer. Friday's original promise is assessed as not met; Monday's revised promise is assessed as met. Both assessments remain attached to their own versions.

| Event | Meaning |
| --- | --- |
| e01 | Original commitment accepted |
| e02 | Provider delay reported Tuesday at 10:00 |
| e03 | Temporary-credential request proposed Tuesday at 11:00 |
| e04 | Evidence observed Tuesday at 09:00, first available Wednesday |
| e05 | Fictional shadow forecast made after Tuesday's noon cutoff |
| e06 | Credential request authorised Wednesday |
| e07 | Monday deadline accepted as version 2 on Thursday |
| e08 | Original Friday promise assessed as not met |
| e09 | Integration deployment completed Monday |
| e10 | Revised Monday promise assessed as met with customer evidence |
| e11 | Changed commitment practice adopted; its effectiveness is still untested |

At `2026-01-06T12:00:00Z`, the snapshot contains exactly **e01, e02, e03**. e04 is excluded despite its earlier occurrence because the predictor did not have it yet. Later actions and revisions are also excluded. Forecast and outcome events are never returned by the initial context utility.

At `2026-01-08T12:00:00Z`, the snapshot contains both accepted versions and the history known by then. It deliberately does not overwrite version 1 with version 2. A future task-specific feature builder must explicitly choose its prediction target and reduce history into features.

Only the stages shown are known. For instance, an `authorised` action does not create an inferred completion event. The example also does not claim the temporary-credential action caused Monday's fulfilment. Actual advice exposure, causal attribution, adjudication of conflicting assessments, and end-to-end training remain future work.
