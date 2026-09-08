# Fictional commitment challenge set

Eight authored scenarios for questioning the commitment abstraction, outcome definitions, and draft data contract. Every event, role, and organisation is invented. There are no partner observations or model-generated forecasts behind these stories.

These are discussion cards, **not training examples, frequency estimates, or a benchmark**. They deliberately include unresolved meanings that the current event contract cannot express fully. No canonical labels are assigned. The number of cases in any category says nothing about how often it occurs in practice.

## Start with the participant's experience

Use the [partner discovery guide](../../docs/partner-discovery.md) before showing the cards. Ask the participant to describe a familiar piece of work in their own vocabulary. Then select two or three relevant cards rather than working through the whole set.

Each card separates what was known at a decision point from what happened later. Pause before revealing the later account. The maintainer discussion is a provisional interpretation, not an answer key. Someone who rejects the scenario or the commitment framing may be exposing the most valuable gap.

| ID | Card | Assumption to challenge |
| --- | --- | --- |
| C01 | [Delivered on time, rejected by the beneficiary](C01-delivered-but-rejected.md) | Recorded delivery and valuable fulfilment mean the same thing |
| C02 | [A responsible cancellation](C02-responsible-cancellation.md) | Stopping a commitment is always failure |
| C03 | [Two promises, one shared resource](C03-competing-commitments.md) | Commitment outcomes can be understood independently |
| C04 | [Late evidence changes the assessment](C04-late-evidence.md) | The latest account was available to earlier decisions |
| C05 | [A warning is followed by successful intervention](C05-forecast-and-intervention.md) | Averted failure proves either model error or model value |
| C06 | [The same words, different promises](C06-disputed-meaning.md) | One accepted record establishes shared meaning and legitimate authority |
| C07 | [Routine fulfilment without an escalation](C07-routine-fulfilment.md) | More recorded activity implies better outcomes |
| C08 | [Valuable work without a bounded promise](C08-work-without-a-promise.md) | Every useful contribution should become a deadline commitment |

## Contract questions to carry into discovery

The [draft 0.1.0 contract](../../docs/data-contract.md) and current validator already preserve accepted versions, occurrence/availability times, and distinct action stages. Free text can describe more than the structured fields can represent. Being able to put a story in a description is not the same as having interoperable semantics for it.

| Cases | What the draft can express | Unresolved research/design question |
| --- | --- | --- |
| C01, C06 | Written criteria, authority references, observations, disputed assessments | Who interprets criteria, which beneficiaries must accept, and how disagreements are adjudicated |
| C02 | A proposal/action to stop and a later learning record | Ratified withdrawal, release of obligations, and effects on beneficiaries |
| C03 | Multiple commitments and dependency references | Shared capacity with units/time, resource contention, and connected evaluation groups |
| C04 | Late observations and multiple assessment events | Which assessment supersedes another, why, and which label was available at each training cutoff |
| C05 | Forecasts and subsequent action records | Actual advice exposure, action selection, spillovers, and causal identification |
| C07 | Known reaffirm/defer actions and supported outcome assessments | How to distinguish low intervention need, missing capture, and unrecorded work |
| C08 | Narrative observations linked to an accepted commitment, if one exists | Whether a bounded commitment is the appropriate unit at all |

This table records **candidate gaps**, not approved requirements or findings about real organisations. Current version remains `0.1.0`; these cards do not change the schema or validator. No card is represented as a schema-valid JSONL fixture. The original [executable trajectory](../README.md) remains the implementation example.

## From a case to a useful discovery

Record the interpretation, an alternative interpretation, the evidence needed to distinguish them, and the consequence for the research. A consequence may be a field change, an observation procedure, a separate target, or an explicit exclusion from scope. Do not assume every ambiguity needs another field.

Use the [case template](TEMPLATE.md) for a new fictional counterexample. Stable IDs make discussion traceable; they do not make interpretations permanent. Keep open questions open until a documented decision changes their status. Partner-informed revisions need permission and enough abstraction to avoid identifying the underlying people or organisation.

## When more synthetic data becomes useful

After reviewing these questions with practitioners, propose generators for specific engineering purposes: timestamp boundary checks, missing-event handling, workload scale, or recovery from conflicting observations. Name the assumed mechanism, vary it deliberately, and document how it could be wrong. Keep generated artefacts separate from partner observations.

Do not select a model architecture because it performs well on labels produced by that same generator. Advancing to a generator should follow a concrete question and reviewed semantics; it does not follow automatically from finishing these eight cards.
