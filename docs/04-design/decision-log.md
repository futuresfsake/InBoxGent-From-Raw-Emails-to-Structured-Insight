# Architecture and Methodology Decision Log

Lightweight ADRs. Status values: Proposed, Accepted, Superseded. New decisions are appended; superseded ones stay for history.

---

## ADR-001: Staged Parquet pipeline with lineage
**Status:** Accepted (2026-11-01)
**Context:** Reruns, debugging and auditability matter more than raw speed at this data size.
**Decision:** Each stage reads and writes Parquet with embedded lineage metadata, separated by quality gates.
**Consequences:** More disk use; stages are independently rerunnable and testable.

## ADR-002: Installable package, notebooks as thin clients
**Status:** Accepted
**Context:** Notebook-only projects hide logic and resist testing.
**Decision:** `src/inboxgent` holds logic; notebooks import it and are paired with `.py` via jupytext.
**Consequences:** Slightly more setup; far better testing and reuse.

## ADR-003: Deduplicate before sampling gold data and before splitting
**Status:** Accepted
**Context:** The Enron corpus contains many copies of the same message across folders. Duplicates across train and test inflate metrics.
**Decision:** Compute exact duplicates on the full corpus before sampling; compute near-duplicate clusters on the sample; split by cluster and thread.
**Consequences:** Extra preprocessing; defensible metrics.

## ADR-004: Freeze cleaned text version before annotation
**Status:** Accepted
**Context:** Span offsets are meaningless if the underlying text changes.
**Decision:** Annotate and evaluate extraction on a specific `clean_version`; store `text_sha256` with labels; any cleaning change creates a new version and requires re-validation.
**Consequences:** Cleaning must be good enough before M4; it also forces disciplined versioning.

## ADR-005: Lock the test partition by hash
**Status:** Accepted
**Context:** Tuning on test data is the most common silent error in applied ML.
**Decision:** Commit a SHA-256 of the sorted test ids before tuning; tune rules, prompts and models on dev only.
**Consequences:** Dev set is small; honest final numbers.

## ADR-006: Commit labels, not email text
**Status:** Accepted
**Context:** Emails are real people's correspondence; redistributing them raises privacy and licensing concerns even if the source is public.
**Decision:** The repo stores message ids, offsets, labels and hashes only; text is rebuilt from the public corpus.
**Consequences:** Rebuild step required; reduced risk.

## ADR-007: Pandera for data contracts, pydantic for LLM outputs
**Status:** Accepted
**Context:** Need schema checks at stage boundaries and structured outputs from LLMs.
**Decision:** Pandera for DataFrames; pydantic for LLM responses and configuration.
**Consequences:** Two validation libraries with clear separate roles; lighter than Great Expectations.

## ADR-008: Temporal plus grouped validation as the default for ML
**Status:** Accepted
**Context:** Random splits leak future and thread information, overstating performance, especially around the 2001 crisis period where distribution shifts.
**Decision:** Primary evaluation uses a temporal holdout with rolling-origin validation and thread/duplicate grouping; a random grouped split is reported to quantify optimism.
**Consequences:** Lower, more honest numbers; potential covariate shift is itself an analysis topic.

## ADR-009: Pin LLM versions and cache raw responses
**Status:** Accepted
**Context:** Hosted models change or retire; temperature 0 is not perfectly deterministic.
**Decision:** Pin model identifiers, version prompts, and archive raw responses used in reported results.
**Consequences:** Reproducibility survives model deprecation; small storage cost.

## ADR-010: No inference of demographic or sensitive attributes
**Status:** Accepted
**Context:** Inferring gender, ethnicity or other sensitive attributes from names or text is unreliable and potentially harmful.
**Decision:** Not performed in any task; slice analyses use non-sensitive attributes (custodian, period, length).
**Consequences:** Some fairness analyses are out of scope and explicitly noted.

## ADR-011: Confirmatory versus exploratory separation
**Status:** Accepted
**Context:** Unlabeled analysis is prone to forking-paths storytelling.
**Decision:** H1-H4 are pre-specified with decision rules and corrected for multiplicity; H5 and other exploratory results are labeled as such.
**Consequences:** Clear epistemic status for each claim.

## ADR-012: Scope tiers with modeling in the core
**Status:** Accepted (supersedes initial plan that treated modeling as optional)
**Context:** For a data science portfolio, predictive modeling with sound validation is a core signal, while network and temporal analysis are valuable extensions.
**Decision:** Core = data engineering, extraction benchmark, predictive modeling, reporting. Extended = topics, network, change points. Stretch = cascade, anomaly, active learning, dashboard.
**Consequences:** Cut order under time pressure is Stretch, then Extended.

## ADR-013: Security baseline delivered in M0
**Status:** Accepted (2026-11-01)
**Context:** The project handles an API key with spend implications, real people's correspondence, third-party dependencies and a public repository. Retrofitting security after data and keys exist is costly and error-prone.
**Decision:** M0 delivers secrets management, access control, supply-chain checks, repo governance and a threat model before any data is downloaded. The pipeline has no user authentication because it has no users; credential and access management replaces it.
**Consequences:** M0 is larger; later milestones start with guardrails already enforced by hooks and CI.

## ADR-014: Restrict reply-prediction to observable replies
**Status:** Accepted
**Context:** The corpus contains only custodian mailboxes; a missing reply may mean no reply or a responder outside the corpus.
**Decision:** T2 includes only messages with at least one custodian among the recipients and excludes messages within W hours of the end of the custodian's data (right-censoring).
**Consequences:** Smaller but cleaner label set; limitations documented.
