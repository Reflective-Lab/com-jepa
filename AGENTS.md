# Working on com-jepa

This is a public research repository. Read README.md, docs/research-plan.md, and the relevant contract before changing behaviour. GitHub Reflective-Lab/com-jepa is the canonical public repository for this project.

Preserve the distinction between implemented code, proposed experiments, and empirical findings. Never fabricate datasets, outcomes, citations, benchmark results, or integration status. Fictional fixtures are for validation only. Prefer the smallest method capable of answering the question; JEPA is a candidate, not a required conclusion.

Keep commitment identity/version, authority, action stage, occurrence time, availability time, and outcome assessment distinct. Do not turn missing evidence into success/failure or let revisions erase an original promise. Forecasts do not confer authority. Personal learning records are outside the initial research export.

Do not import private source, internal endpoints, partner data, credentials, or personal work records. Use publicly available references and wholly fictional examples. Never publish real data or trained artefacts without explicit authorisation and a documented release review.

Run `.venv/bin/python -m unittest discover -s tests -v` and `.venv/bin/python -m com_jepa validate examples/fictional-trajectory.jsonl` for code/schema changes. Maintainer work uses the existing checkout on `main`: pull before asserting state, validate, commit, and push authorised changes to the canonical GitHub repository. Do not create additional branches or worktrees. External pull requests may be reviewed and merged into `main`; remove merged topic branches once their commits are preserved. Do not push, merge, or publish a release without task authorisation.

For releases, update README status and run instructions, CHANGELOG.md, and CITATION.cff. Keep schema versions separate from release bookkeeping. Tag the validated main commit with an annotated `vX.Y.Z` tag, publish matching release notes, and synchronise experiment checkouts to that commit. Never move a published release tag.
