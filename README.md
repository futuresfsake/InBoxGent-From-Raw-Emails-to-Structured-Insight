# InBoxGent: From Raw Emails to Structured Insight

An end-to-end, evidence-driven data science study on the public Enron email corpus. It turns raw, noisy email into validated structured data, benchmarks competing information-extraction systems under a rigorous protocol, builds leakage-safe predictive models on the result, and analyzes the communication network and its evolution over time.

> **Status:** design and methodology phase. No implementation yet. The full plan, hypotheses and evaluation protocol are in [`docs/`](docs/).

## Research questions

| # | Question | Track |
|---|---|---|
| RQ1 | How reliably can raw email be converted into clean, deduplicated, thread-aware structured data, and how much does cleaning matter downstream? | Data engineering |
| RQ2 | Which extraction approach (rules, classic NLP, small LLM, larger LLM) gives the best accuracy per dollar for people, organizations, dates, amounts and action items? | Information extraction |
| RQ3 | Can we predict email category and reply behavior under realistic (temporal, grouped) validation, and do extracted fields add predictive value? | Predictive modeling |
| RQ4 | What themes, network structure and structural breaks does the corpus reveal, and do they align with known external events? | Exploratory and network analysis |

Hypotheses, metrics and decision rules are fixed before looking at test data. See [`docs/01-overview/problem-framing.md`](docs/01-overview/problem-framing.md).

## What makes this a data science project

- Pre-specified hypotheses and analysis plan, with exploratory work clearly labeled as such
- Datasheet documenting dataset provenance, bias and known defects
- Frozen dev/test split for the labeled set, with measured inter-annotator agreement
- Bootstrap confidence intervals and paired significance tests, not single-number leaderboards
- Leakage controls: deduplication before splitting, thread-grouped and temporal validation
- Ablations, calibration, error analysis and a cost-quality trade-off analysis
- Reproducible pipeline with data-quality gates, experiment tracking and pinned environments
- Ethics and privacy plan for working with real people's email

## Scope tiers

| Tier | Contents |
|---|---|
| Core | Ingest, parsing, cleaning, dedup, threading, EDA, gold set, extraction benchmark, predictive modeling, findings report |
| Extended | Topic modeling with stability analysis, network analysis, change-point detection |
| Stretch | Hybrid extraction ensemble, anomaly detection, active learning for labeling, Streamlit dashboard |

## Documentation map

| Area | Folder | Contents |
|---|---|---|
| Overview | [`docs/01-overview`](docs/01-overview/) | Project overview, problem framing and hypotheses |
| Requirements | [`docs/02-requirements`](docs/02-requirements/) | Requirements specification, user stories |
| Tech | [`docs/03-tech`](docs/03-tech/) | Tech stack, reproducibility and MLOps, security and threat model |
| Design | [`docs/04-design`](docs/04-design/) | HLD, LLD, architecture decision log |
| Data science | [`docs/05-data-science`](docs/05-data-science/) | Dataset datasheet, evaluation methodology, modeling plan, ethics and privacy |
| Planning | [`docs/06-planning`](docs/06-planning/) | Milestones, status, reference, stories, testing, risks, open questions, [gap register](docs/06-planning/gap-register.md), [delivery workflow (DoR, DoD, push pipeline)](docs/06-planning/delivery-workflow.md) |

## Planned repository layout

```
inboxgent/
├── pyproject.toml, Makefile, config/
├── src/inboxgent/    ingest, parse, cleaning, dedup, threading, extract/, evaluate/, models/, analysis/
├── notebooks/        one question per notebook, paired via jupytext
├── tests/
├── data/             raw/ interim/ labeled/ outputs/   (only labeled/ is committed)
├── reports/          figures/, findings.md, model_card.md
└── docs/
```

## References

- Klimt, B., Yang, Y. (2004). The Enron Corpus: A New Dataset for Email Classification Research.
- Gebru et al. (2021). Datasheets for Datasets.
- Mitchell et al. (2019). Model Cards for Model Reporting.
- Kapoor, S., Narayanan, A. (2023). Leakage and the reproducibility crisis in machine-learning-based science.
