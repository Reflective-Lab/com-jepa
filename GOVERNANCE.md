# Project governance

## Purpose and stewardship

Reflective Lab initiates com-jepa as an open research effort. Kenneth Pernyér is the initial maintainer. GitHub `Reflective-Lab/com-jepa` is the canonical public repository. The project is independently usable; access to Reflective's private applications or platform is not required.

The maintainer reviews and accepts changes. Proposed experiments, contract changes, and interpretation of results should be discussed publicly with enough evidence for others to challenge them. A merged proposal is not proof that its hypothesis is true.

## Decisions and review

Use issues to define a question and pull requests to propose a concrete change. Record consequential research decisions with the alternatives considered, the reason, and the evidence that would justify revisiting them. Keep implementation status, design intentions, and observed findings distinct.

Changes to target semantics, lineage, timestamp rules, or data access require updated documentation and validation examples. Empirical reports must identify a frozen dataset/split, baselines, information access, uncertainty, and limitations. A result that supports a simple model or rejects JEPA belongs in the project on equal terms.

Initial bootstrapping establishes the default branch. Subsequent substantive work should use pull requests. Stable releases and any shared data/model release require an explicit scope and review; the current draft version is not a production support commitment.

## Independence and attribution

Declare relevant organisational affiliations, funding, commercial interests, and dataset restrictions when proposing an experiment or reporting a result. Reflective's commercial interests do not substitute for evidence. Partnership does not require public disclosure of confidential operational information.

Use [CONTRIBUTORS.md](CONTRIBUTORS.md) for opt-in attribution. Agree authorship separately for each publication. External papers remain the work of their authors and should be cited directly.

## Participation and sensitive matters

Participation follows the [code of conduct](CODE_OF_CONDUCT.md). The maintainer handles moderation and can close or remove material that violates it. Sensitive reports use the private route in [SECURITY.md](SECURITY.md). A real-data pilot requires its own participant, access, and stewardship arrangements; a GitHub contribution is not permission to pool an organisation's data.
