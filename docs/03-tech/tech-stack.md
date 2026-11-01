# Tech Stack

## Summary

| Area | Choice | Reason |
|---|---|---|
| Language | Python 3.11+ | Ecosystem breadth, reviewer familiarity |
| Packaging and environment | `pyproject.toml`, `uv` (or pip-tools) with a lock file | Reproducible installs |
| Data handling | pandas, pyarrow (Parquet) | Stage artifacts in columnar format |
| Ad hoc analytics | DuckDB | SQL over Parquet for fast profiling |
| Schema validation | pandera, pydantic | Typed data contracts at stage boundaries and for LLM outputs |
| Email parsing | stdlib `email`, `dateutil` | Robust RFC 822 handling |
| Near-duplicate detection | `datasketch` (MinHash/LSH) | Scalable approximate matching |
| PII detection | Microsoft Presidio plus custom regex | Redaction in published artifacts |
| Rule-based extraction | regex, `dateparser` | Transparent baseline |
| Classic NLP | spaCy (`en_core_web_sm`, optional `en_core_web_trf`) | Standard NER baseline |
| LLM extraction | Anthropic API: `claude-haiku-5-5` (small) and `claude-sonnet-5-5` (larger) | Cost-quality comparison across tiers; swappable behind an interface |
| Classical ML | scikit-learn, LightGBM | Linear and boosted models, pipelines, CV |
| Embeddings | sentence-transformers | Local, no per-call cost |
| Interpretability | SHAP, permutation importance | Model explanations |
| Calibration | scikit-learn calibration, custom ECE | Probability quality |
| Topic modeling | BERTopic (UMAP + HDBSCAN), gensim for coherence | Topic discovery with an established coherence metric |
| Network analysis | NetworkX, python-igraph / leidenalg | Centrality and community detection |
| Change-point detection | `ruptures` (PELT, binary segmentation) | Standard offline change-point methods |
| Statistics | SciPy, statsmodels | Bootstrap, McNemar, permutation tests, multiplicity correction |
| Experiment tracking | MLflow (local file store) | Run lineage for parameters, metrics, artifacts |
| Visualization | matplotlib, seaborn, plotly | Static report figures and interactive charts |
| Dashboard (stretch) | Streamlit | Fast shareable app |
| Notebooks | Jupyter with `jupytext` pairing and `nbstripout` | Clean diffs, no committed outputs with data |
| Testing | pytest, pytest-cov, hypothesis | Unit and property-based tests |
| Quality | ruff, mypy (selected modules), pre-commit, `detect-secrets` | Style, types, secret scanning |
| Automation | Makefile for stages, GitHub Actions for lint and tests | Reproducible commands and CI |
| Version control | Git and GitHub, milestone tags | Small commits, traceable history |

## Principles
1. **Logic in the package, narrative in notebooks.** Notebooks import from `inboxgent` and never contain core logic.
2. **Stage artifacts are immutable and versioned.** Each stage reads Parquet and writes Parquet plus a lineage record.
3. **Contracts at boundaries.** Pandera schemas for tables, pydantic models for LLM responses.
4. **One interface, many systems.** Extractors share an interface so evaluation code is system-agnostic.
5. **Determinism where possible.** Seeds, temperature 0, cached LLM responses, pinned model identifiers.
6. **Secrets stay out of the repo.** Keys via environment variables only.

## Data zones

```
data/
  raw/       (git-ignored)  original corpus + manifest
  interim/   (git-ignored)  parsed, cleaned, threaded Parquet
  features/  (git-ignored)  modeling tables
  labeled/   (committed)    gold labels and message ids only, no text
  outputs/   (git-ignored)  predictions, metrics, LLM cache
```

## Alternatives considered

| Option | Why not chosen (for now) |
|---|---|
| Polars instead of pandas | Faster, but pandas is more widely read by reviewers; DuckDB covers heavy queries |
| Great Expectations | Heavier than needed for a single-developer project; pandera is lighter |
| DVC for data versioning | Corpus is public and re-downloadable; checksum manifest is sufficient initially |
| Local LLM via Ollama as a fifth system | Adds breadth but also scope; kept as optional extension |
| Gensim LDA as primary topic model | Lower coherence on short text; kept only as a comparison baseline if time allows |
| Fine-tuned transformer NER | Requires more labeled data than the gold set; revisit if active learning is added |
