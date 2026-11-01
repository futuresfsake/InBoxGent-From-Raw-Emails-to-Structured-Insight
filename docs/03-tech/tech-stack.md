# Tech Stack

## Summary

| Area | Choice | Reason |
|---|---|---|
| Language | Python 3.11+ | Standard for data science, richest ecosystem |
| Data handling | pandas, pyarrow (Parquet) | Familiar, fast columnar storage between stages |
| Email parsing | stdlib `email`, `mailparser` if needed | Handles RFC 822 without extra weight |
| Cleaning | regex, `email-reply-parser` style heuristics | Transparent, auditable rules |
| Classic NLP | spaCy | NER and tokenization baseline |
| LLM extraction | Anthropic API (Claude) | Strong structured extraction; swap-able behind an interface |
| ML | scikit-learn | TF-IDF, logistic regression, cross-validation |
| Embeddings | sentence-transformers | Local, no API cost |
| Topics / clustering | BERTopic or KMeans + UMAP | Interpretable topic discovery |
| Visualization | matplotlib, seaborn, plotly | Static report figures plus interactive charts |
| Dashboard (stretch) | Streamlit | Fastest path to a shareable app |
| Notebooks | Jupyter | Narrative analysis |
| Testing | pytest | Unit tests for `src/` |
| Quality | ruff, pre-commit | Consistent style |
| Environment | venv + `requirements.txt` | Simple and reproducible |
| Version control | Git + GitHub | Small, frequent commits |

## Design principles
- Logic in `src/`, orchestration in notebooks.
- Each pipeline stage reads and writes Parquet so stages can be rerun independently.
- Extraction backends implement one shared interface so evaluation code does not care which one ran.
- Secrets (API keys) come from environment variables, never from the repo.

## Data storage layout
```
data/
  raw/        (git-ignored) original Enron files
  interim/    (git-ignored) parsed and cleaned Parquet
  labeled/    (committed) gold-standard sample
  outputs/    (git-ignored) predictions and metrics
```

## Alternatives considered
- **Polars instead of pandas:** faster, but pandas is more widely recognized by reviewers.
- **Local LLM (Ollama) instead of API:** zero cost, lower accuracy; kept as an optional fourth backend.
- **Gensim LDA instead of BERTopic:** older, less coherent topics on short text.
