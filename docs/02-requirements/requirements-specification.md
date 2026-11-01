# Requirements Specification

IDs: FR = functional, NFR = non-functional. Priority: M = must, S = should, C = could.

## Functional requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Load raw Enron emails and sample a configurable subset with a fixed random seed. | M |
| FR-02 | Parse RFC 822 headers (From, To, Cc, Date, Subject, Message-ID). | M |
| FR-03 | Remove signatures, quoted replies and forwarded chains from the body. | M |
| FR-04 | Normalize encodings and whitespace. | M |
| FR-05 | Deduplicate messages (exact and near-duplicate). | M |
| FR-06 | Log per-step counts of what was removed or changed. | M |
| FR-07 | Extract dates, monetary amounts, organizations and people from body text. | M |
| FR-08 | Provide three extraction backends: rules, classic NLP, LLM. | M |
| FR-09 | Provide a labeled evaluation set of about 200 emails. | M |
| FR-10 | Compute precision, recall and F1 per field and per backend. | M |
| FR-11 | Record cost and latency per backend. | S |
| FR-12 | Produce EDA: volume over time, sender network, length and response-time distributions. | M |
| FR-13 | Train an email classifier (TF-IDF + logistic regression baseline, embedding variant). | M |
| FR-14 | Discover topics via topic modeling or embedding clusters. | S |
| FR-15 | Provide an interactive dashboard to explore results. | C |

## Non-functional requirements

| ID | Requirement | Priority |
|---|---|---|
| NFR-01 | Reproducibility: fixed seeds, pinned dependencies, documented run order. | M |
| NFR-02 | Privacy: only public data in the repo; raw data directory is git-ignored. | M |
| NFR-03 | Modularity: logic lives in `src/`, notebooks only orchestrate and display. | M |
| NFR-04 | Testability: core cleaning and evaluation functions have unit tests. | S |
| NFR-05 | Performance: cleaning a 50k-email sample completes in under 15 minutes on a laptop. | S |
| NFR-06 | Cost control: LLM extraction runs only on the labeled set and a capped sample. | M |
| NFR-07 | Documentation: every notebook starts with its question and ends with a conclusion. | S |

## Constraints
- Single developer, part-time.
- Laptop-class hardware, no GPU assumed.
- LLM usage limited by API budget.

## Assumptions
- Enron corpus remains freely available.
- A 200-email labeled set is enough to compare backends meaningfully.
