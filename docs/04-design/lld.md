# Low-Level Design (LLD)

## Repository layout
```
InBoxGent/
├── config.py
├── data/            raw/ interim/ labeled/ outputs/
├── notebooks/       01_eda, 02_cleaning, 03_extraction_eval, 04_modeling, 05_topics
├── src/
│   ├── ingest.py
│   ├── parse.py
│   ├── cleaning.py
│   ├── extract/
│   │   ├── base.py
│   │   ├── rules.py
│   │   ├── spacy_backend.py
│   │   └── llm_backend.py
│   ├── evaluate.py
│   └── analysis/    eda.py, classify.py, topics.py
├── tests/
├── reports/         figures/, findings.md
└── docs/
```

## Data schemas

### emails_parsed
| Column | Type | Notes |
|---|---|---|
| message_id | str | primary key |
| date | datetime (UTC) | parsed from header |
| sender | str | normalized address |
| recipients | list[str] | To + Cc + Bcc, flattened |
| subject | str | |
| body_raw | str | unmodified body |
| folder | str | origin mailbox folder |

### emails_clean (adds)
| Column | Type | Notes |
|---|---|---|
| body_clean | str | after all cleaning steps |
| is_duplicate | bool | flagged, not silently dropped |
| n_chars_removed | int | audit metric |

### Extraction output (long format)
| Column | Type |
|---|---|
| message_id | str |
| backend | str (`rules`, `spacy`, `llm`) |
| field | str (`person`, `org`, `date`, `amount`, `action_item`) |
| value | str |
| span_start, span_end | int, nullable |

### Gold labels
Same schema as extraction output, plus `annotator` and `labeled_at`.

## Key interfaces

```python
# src/extract/base.py
class Extractor(Protocol):
    name: str
    def extract(self, message_id: str, text: str) -> list[ExtractedItem]: ...

@dataclass
class ExtractedItem:
    message_id: str
    field: str
    value: str
    span: tuple[int, int] | None = None
```

```python
# src/cleaning.py
def clean_body(text: str) -> tuple[str, CleaningStats]: ...
def run_cleaning(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Returns (cleaned dataframe, per-step log)."""
```

```python
# src/evaluate.py
def score(pred: pd.DataFrame, gold: pd.DataFrame, match: str = "normalized") -> pd.DataFrame:
    """Per-field precision, recall, F1."""
```

## Cleaning step order
1. Decode and normalize unicode, whitespace
2. Remove forwarded-message blocks
3. Remove quoted replies (`>` prefixes, "On ... wrote:" blocks)
4. Remove signatures and legal disclaimers
5. Collapse blank lines
6. Flag exact duplicates (hash), then near-duplicates (MinHash)

Each step records rows affected and characters removed.

## Matching rules for evaluation
- Normalize case, whitespace, and punctuation before comparing.
- Dates compared as parsed values; amounts compared as numbers plus currency.
- Entity match is exact on normalized string by default; a lenient mode allows token-overlap match and is reported separately.

## Classification design
- Labels: `business` vs `personal` (and optionally urgent/routine), derived from a hand-labeled sample plus folder heuristics, documented in the notebook.
- Features: TF-IDF (baseline) and sentence embeddings.
- Model: logistic regression, 5-fold stratified cross-validation, final held-out test split.
- Baselines: majority class and TF-IDF + LR.

## Topic modeling design
- Embed `body_clean` with a sentence-transformer.
- Reduce with UMAP, cluster with HDBSCAN (BERTopic), or KMeans as a fallback.
- Report top terms per topic and a 2-D UMAP plot.

## Error handling
- Malformed headers: keep the row, set fields to null, count in the log.
- LLM failure or timeout: retry with backoff, then record an empty result and a failure flag.
- All errors counted in stage summary logs.

## Caching
LLM responses stored by hash of (model, prompt, text) in `data/outputs/llm_cache/`.
