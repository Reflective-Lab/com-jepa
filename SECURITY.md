# Security and responsible disclosure

## Scope and support

com-jepa is an early research repository with a draft schema, local validation utility, and fictional examples. It is not a production service, a secure data store, an authorisation engine, or an approved environment for processing sensitive organisational data.

The current default branch is the supported development line. There are no production releases or long-term support guarantees. Schema validation checks record structure and selected temporal relationships; it cannot verify the truth of evidence, enforce an organisation's authority, anonymise a dataset, or certify a model as safe.

## Report privately

Use GitHub's [private vulnerability reporting](https://github.com/Reflective-Lab/com-jepa/security/advisories/new) for a suspected vulnerability, accidental sensitive-data disclosure, or a bypass that could leak future or private information into research outputs. Avoid a public issue when the report contains sensitive details.

Include the affected commit, expected and actual behaviour, a minimal fictional reproducer, and the likely impact. Do not attach real organisational records, access tokens, credentials, or personal data. Coordinate any necessary evidence exchange privately with the maintainer after the initial report.

The maintainer will assess reports and coordinate a correction and disclosure where appropriate. This volunteer research project cannot promise a response or remediation deadline. If the GitHub form is unavailable, contact the maintainer through the public channels on [Reflective's website](https://www.reflective.se) and request a private reporting route before sharing details.

## Data and model handling

- Keep real data, evidence documents, credentials, and model checkpoints out of this public repository. Ignore rules are a convenience, not a security boundary.
- Treat free text, embeddings, and graph structure as potentially identifying even when direct identifiers are removed.
- Run the utility on bounded, trusted research exports. It loads an export into memory and is not hardened for hostile or arbitrarily large input.
- Use isolated environments and reviewed dependencies. CI needs no organisational data, cloud credentials, or model-provider keys.

Ordinary modelling limitations and methodological disagreements belong in public research issues using fictional examples. See [data stewardship](docs/data-contract.md#data-stewardship) for the proposed handling of a real pilot.
