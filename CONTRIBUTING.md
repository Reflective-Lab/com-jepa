# Contributing

Start with a question we can test, a fictional example that breaks the contract, a better baseline, or a correction to a supported claim. Open an issue or a pull request with the problem, proposed artefact, evidence, and what would count against the proposal.

The first priorities are in [First 90 days](docs/first-90-days.md). Organisational practitioners, process-mining researchers, applied-ML and JEPA researchers, application developers, and human–AI interaction researchers can contribute independently.

For code or schema changes, run the README commands. Include tests when changing temporal boundaries, lineage, target semantics, or validation behaviour. Update the schema version and examples when the contract changes. The draft may change incompatibly during 0.x releases. Maintainer work proceeds on the canonical `main` checkout; external contributors can submit pull requests. Releases are annotated tags on validated `main` commits, with matching README, changelog, and citation metadata.

Publish only fictional or separately cleared data. Do not paste private work records, personal data, credentials, or partner identifiers into issues, examples, model artefacts, or pull requests. Propose the collection method publicly and keep any real-data arrangement separate. See [Data stewardship](docs/data-contract.md#data-stewardship).

Report empirical work with dataset provenance and rights, target and exclusion rules, temporal/group splits, information access, baseline and tuning budgets, uncertainty, and limitations. Label synthetic results as pipeline checks. Negative results are welcome. Do not imply causality, broad transfer, or human learning from predictive accuracy alone.

Contributions of original material are under the repository's MIT licence. Identify external material and its licence; do not copy papers or datasets into this repository without the required rights.
