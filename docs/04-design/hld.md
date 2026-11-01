# High-Level Design (HLD)

## Architecture overview
InBoxGent is a staged batch pipeline. Each stage consumes the previous stage's Parquet output and produces its own, so any stage can be rerun in isolation.

```
 Raw Enron files
        |
        v
 [1 Ingest & Sample] --> interim/emails_raw.parquet
        |
        v
 [2 Parse Headers]   --> interim/emails_parsed.parquet
        |
        v
 [3 Clean Body]      --> interim/emails_clean.parquet  (+ cleaning_log.csv)
        |
        +-----------------------------+
        v                             v
 [4 Extraction]                [6 Analysis]
   rules | spaCy | LLM            EDA, classification, topics
        |                             |
        v                             v
 [5 Evaluation vs gold set]    reports/figures, findings.md
        |
        v
 outputs/metrics.csv  ---> [7 Dashboard (stretch)]
```

## Components

| # | Component | Responsibility | Module |
|---|---|---|---|
| 1 | Ingest | Read raw files, seeded sampling | `src/ingest.py` |
| 2 | Parser | Headers to structured columns | `src/parse.py` |
| 3 | Cleaner | Strip signatures, quotes, forwards; normalize; dedupe; log | `src/cleaning.py` |
| 4 | Extractors | Three interchangeable backends behind one interface | `src/extract/` |
| 5 | Evaluator | Compare predictions to gold labels, compute metrics | `src/evaluate.py` |
| 6 | Analysis | EDA, classifier, topic modeling | `src/analysis/`, notebooks |
| 7 | Dashboard | Interactive exploration (stretch) | `app/` |

## Key design decisions
1. **Staged Parquet artifacts** rather than one monolithic script: supports reruns, debugging and clear lineage.
2. **Common extractor interface** so the evaluator treats all backends identically and a new backend is one new file.
3. **Cleaning log as a first-class output** to make every removal auditable.
4. **Gold set committed, raw data not**: protects the repo from size and licensing issues while keeping evaluation reproducible.
5. **LLM calls isolated and cached** to control cost and allow deterministic reruns.

## Data flow summary
Raw text -> structured headers -> clean body -> entities/fields -> metrics and insights.

## External dependencies
- Enron corpus (download)
- Anthropic API (LLM backend only)
- Hugging Face model hub (embeddings download)

## Cross-cutting concerns
- **Reproducibility:** global seed in `config.py`, pinned requirements.
- **Logging:** Python `logging` with per-stage summaries.
- **Configuration:** single `config.py` for paths, sample size, model names.
- **Security/privacy:** API keys via environment; no private mail processed.
