# Draft commitment data contract

Version `0.1.0`. This is a research export proposal, not a production Organisation Core specification. The executable [event schema](../schemas/event.schema.json) is deliberately narrower than the full research agenda. Schema validity does not prove consent, factual accuracy, causal identification, or dataset completeness.

## The unit: a commitment trajectory

An organisation owns a stable commitment ID. Accepted versions preserve the promise, beneficiaries, accountable role, authority reference, acceptance criteria, deadline, assumptions, and dependency references. A revision creates a new version with a reason and a link to its predecessor. It does not overwrite the original promise.

Capture transitions when they happen; avoid retrospectively inventing a smooth story. The first export has seven event types:

| Event | Required meaning |
| --- | --- |
| `commitment.accepted` | Version 1 of a ratified commitment; what, for whom, by when, and under whose authority |
| `commitment.revised` | A later accepted version, its predecessor, and the reason for change |
| `action.recorded` | A typed action, its identity, stage, actor role, and relevant authority |
| `observation.recorded` | Evidence of a condition, its subject, quality, and provenance |
| `outcome.assessed` | An assessment of fulfilment by the exact version's deadline, with evidence and explicit uncertainty |
| `forecast.recorded` | A model/human forecast of that target, its context cutoff, version, and planned exposure |
| `learning.recorded` | A proposed or adopted change, or a later assessment of it, connected to prior evidence |

The envelope carries `organisation_id`, `initiative_id`, `commitment_id`, `commitment_version`, `event_id`, `source_ref`, `occurred_at`, and `available_at`. Roles and identifiers in the example are fictional. Production identifiers should be pseudonymous within a governed export; pseudonymisation alone does not make trajectories anonymous.

`occurred_at` means when the recorded action, observation, acceptance, or assessment happened. `available_at` means when this information was first available to the designated prediction system. An observation made on Monday but received on Wednesday is unavailable to Tuesday's prediction. Deadline and proposed future actions belong in payloads; do not timestamp an unexecuted plan as if it already happened.

The draft requires UTC timestamps, second precision, and `available_at >= occurred_at`. If legacy systems cannot supply availability, mark that dataset unsuitable for prospective replay until a defensible conservative rule is documented. Do not substitute occurrence time silently.

## What actions should mean

Start with a small, reviewable vocabulary:

| Family | Examples |
| --- | --- |
| `investigate_clarify` | Test an assumption; clarify acceptance criteria |
| `authorise_assign` | Approve a proposal; assign accountable ownership |
| `allocate_sequence` | Allocate capacity; change execution order |
| `coordinate_unblock` | Resolve a dependency; renegotiate a handoff |
| `execute_deliver` | Implement; deliver; provide a service |
| `revise_stop` | Propose revising, withdrawing, or stopping work |
| `reaffirm_defer` | Explicitly maintain a decision or defer action |
| `other` | A described action the vocabulary does not yet cover |

An action's lifecycle is separate: `proposed`, `authorised`, `started`, `completed`, or `abandoned`. An authorised action is not evidence it happened. A completed action is not evidence the commitment was fulfilled. A proposal to revise does not itself create a ratified version.

No recorded action can mean missing capture; it is not automatically an observed decision to do nothing. Use an explicit reaffirm/defer record for a known decision of that kind. Missing stage events remain missing; this export does not infer them.

Future embeddings can combine action family and stage with the target commitment, temporal context, resources, uncertainty, and dependency structure. Similarity must not substitute for typed authority. Have practitioners independently code examples and revise the vocabulary when it conflates distinct actions.

## Outcomes and promises

The initial label assesses **all criteria of one version by its deadline**. `met` and `not_met` require supporting evidence and an assessment at or after that deadline. `unknown`, `right_censored`, and `disputed` remain separate. Early fulfilment can be recorded as an observation; the benchmark assessment waits until the fixed deadline to avoid inconsistent label timing.

An assessment of `not_met` means evidence establishes that at least one criterion was unmet at the deadline. The absence of a completion event is insufficient. A later successful delivery does not retroactively change this label. Append a new assessment if earlier evidence was wrong; never silently overwrite the history. A final benchmark needs an explicit adjudication and assessment-selection policy, which the current snapshot utility does not implement.

Revised commitments retain original and new deadlines and independent assessments. Cancellation, partial acceptance, costs of revision, and long-lived obligations need extensions before they become benchmark targets; do not force them into this first binary task. The first schema covers individual assessment records, not an exhaustive organisational ontology.

## Separate context from targets

For cutoff *t*, predictor context may include accepted versions, actions, observations, and learning records only when both timestamps are at or before *t*. Future outcome assessments are training targets, never predictor inputs. The initial utility also excludes all forecasts and all outcome assessments as a conservative boundary. A future governed feature builder may explicitly incorporate prior settled outcomes and prior forecasts, with their own leakage controls.

A deadline in an accepted promise is known future intent and is allowed. A future completed action is not. Training labels may become available after the forecast cutoff, but must be available by the model's training cutoff. Every benchmark must retain both cutoffs.

The utility emits context events only: it is not a full feature builder, label joiner, or state reducer. It does not choose the latest commitment version or collapse action history. It rejects incomplete version lineage within an export so callers cannot silently replay a revision without its original promise.

## Additional collection proposed for a pilot

Add fields only when they support a question and can be collected responsibly:

- Resource constraints with units, confidence, and effective dates; dependency edges with type, source, and observed state.
- Criterion-level evidence and beneficiary acceptance; partial fulfilment and realised value; disputes and adjudication history.
- Alternatives considered, assumptions challenged, relevant dissent, and why an intervention was selected.
- Actual advice exposure and subsequent intervention, distinct from the forecast's initial exposure setting. The draft forecast event is insufficient for a live advice trial.
- Capture-system changes, missingness reasons, action costs, and a complete observation plan. Records from one app alone may omit the work that matters most.

The current schema cannot represent every item above. Extend it with versioned examples and tests before claiming an adapter collects them. The Organisation Core can be richer than a particular research export.

## Data stewardship

Public examples must be wholly fictional or independently cleared for publication. Do not submit meeting transcripts, customer names, employee identifiers, credentials, private URLs, or exported work records through public issues or pull requests. Free text and graph structure can identify people and organisations even after names are removed.

A real pilot needs a documented purpose, authorised participation, access and retention rules, correction/deletion handling, and an agreed route for participants to challenge data and uses. Keep raw evidence in its source system when possible. Export only the minimum necessary features and controlled provenance references. Cross-organisation training requires separate permission and disclosure review; it is not implied by participation in local research.

Exclude individual learning-card answers, personal recall schedules, private reflections, and employee performance rankings from the initial dataset. Evaluate organisational conditions and commitment trajectories. Models and derived embeddings can retain sensitive information and need the same deliberate handling as other research artefacts.
