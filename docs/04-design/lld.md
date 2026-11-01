# Low-Level Design (LLD)

## 1. Repository layout

```
inboxgent/
├── pyproject.toml, Makefile, .pre-commit-config.yaml
├── config/                  default.yaml, prompts/ (versioned), events.yaml
├── src/inboxgent/
│   ├── config.py, cli.py, logging.py
│   ├── ingest.py, parse.py, cleaning.py, dedup.py, threading.py
│   ├── quality.py, privacy.py, tracking.py
│   ├── annotation/          sampling.py, agreement.py
│   ├── extract/             base.py, rules.py, spacy_backend.py, llm_backend.py, cascade.py
│   ├── evaluate/            matching.py, metrics.py, bootstrap.py, tests.py, errors.py
│   ├── features.py
│   ├── models/              baselines.py, boosted.py, embedding.py, calibration.py, splits.py
│   ├── analysis/            eda.py, topics.py, network.py, changepoint.py, anomaly.py
│   └── reporting.py
├── notebooks/               01_eda ... 08_synthesis (paired .py via jupytext)
├── tests/                   unit/, property/, integration/, fixtures/
├── data/                    raw/ interim/ features/ labeled/ outputs/
├── reports/                 figures/, tables/, findings.md, model_card.md
└── docs/
```

## 2. Data schemas

### `emails_parsed`
| Column | Type | Notes |
|---|---|---|
| message_id | str | key; synthesized hash if header missing |
| custodian | str | mailbox owner from path |
| folder | str | origin folder |
| date_utc | datetime64[ns, UTC], nullable | parse failures nulled and counted |
| sender | str | normalized lower-case address |
| recipients_to / cc / bcc | list[str] | normalized |
| n_recipients | int | derived |
| subject | str | raw |
| subject_norm | str | stripped of Re:/Fw: prefixes, lower-cased |
| body_raw | str | unmodified |
| sample_stratum | str | custodian x year |
| inclusion_prob | float | for weighted analysis if needed |

### `emails_clean` (adds)
| Column | Type | Notes |
|---|---|---|
| clean_version | str | e.g. `clean_v3`; part of every downstream key |
| body_clean | str | final cleaned text |
| chars_removed_by_step | dict[str,int] | audit |
| text_sha256 | str | detects drift against gold annotations |
| dup_cluster_id | str | exact and near duplicates |
| is_canonical | bool | one per cluster |
| thread_id | str | reconstructed |
| thread_conf | float | confidence of assignment |
| pii_flags | list[str] | detected categories |

### `gold_labels` (committed, no text)
| Column | Type | Notes |
|---|---|---|
| message_id | str | |
| clean_version | str | text version annotated |
| text_sha256 | str | must match rebuilt text |
| partition | str | `dev` or `test`; test hashed and locked |
| field | str | person, organization, date, amount, action_item |
| start, end | int | character offsets in `body_clean` |
| surface | str | optional; omitted for amounts or dates if considered sensitive |
| norm_value | str | normalized date (ISO) or amount (value + currency) |
| annotator | str | A or B |
| adjudicated | bool | final label flag |

### `extractions` (long format, one row per predicted item)
message_id, system, run_id, field, start, end, norm_value, confidence (nullable), failure_flag.

### `ml_table_t2`
message_id, thread_id, custodian, date_utc, label_reply_w24, label_reply_w72, censored (bool), metadata features, text features reference, extracted features (F3 group), split_assignment per scheme.

### `results`
run_id, task, system or model, split_scheme, metric, value, ci_low, ci_high, n_emails, n_items.

## 3. Interfaces

```python
@dataclass(frozen=True)
class Span:
    message_id: str
    field: str          # person | organization | date | amount | action_item
    start: int
    end: int
    norm_value: str | None = None
    confidence: float | None = None

class Extractor(Protocol):
    name: str
    version: str
    def extract(self, message_id: str, text: str) -> list[Span]: ...
    def extract_batch(self, rows: Iterable[tuple[str, str]]) -> list[Span]: ...
```

```python
# evaluate/metrics.py
def score(pred: pd.DataFrame, gold: pd.DataFrame, *, match: Literal["strict","lenient"]) -> pd.DataFrame: ...

# evaluate/bootstrap.py
def cluster_bootstrap(
    pred: pd.DataFrame, gold: pd.DataFrame, *, metric: Callable,
    n_boot: int = 10_000, seed: int, cluster_col: str = "message_id",
) -> BootstrapResult: ...

def paired_bootstrap_diff(
    pred_a: pd.DataFrame, pred_b: pd.DataFrame, gold: pd.DataFrame, *,
    metric: Callable, n_boot: int = 10_000, seed: int,
) -> BootstrapResult: ...   # resamples emails once, evaluates both systems on the same resample
```

```python
# models/splits.py
def temporal_split(df, *, date_col, train_q, val_q) -> SplitIndices: ...
def rolling_origin(df, *, date_col, n_folds, group_col) -> Iterator[SplitIndices]: ...
def grouped_random_split(df, *, group_col, seed) -> SplitIndices: ...
def assert_no_leakage(split: SplitIndices, df: pd.DataFrame) -> None: ...
```

## 4. Algorithms and parameters

### Cleaning (ordered)
1. Unicode normalization (NFKC), control-character removal, whitespace collapse
2. Forward block removal: header markers like `-----Original Message-----`, `---- Forwarded by ...`
3. Quoted-reply removal: `>` prefixed lines, `On <date>, <name> wrote:` blocks, and header-style quoted blocks
4. Signature and disclaimer removal: delimiter heuristics (`--`), trailing contact blocks, known legal boilerplate learned from frequent trailing n-grams
5. Final whitespace normalization
Each step logs characters removed. Heuristics are validated on the manual audit; frequent-boilerplate list is derived from the data and reviewed by hand.

### Deduplication
- **Exact:** hash of normalized (sender, subject_norm, body_clean).
- **Near:** MinHash with 5-word shingles, 128 permutations, LSH candidate generation; Jaccard threshold initial 0.85, chosen by precision/recall on a labeled pair sample.
- **Canonical selection:** earliest message in the cluster, preferring a sent-mail folder copy.
- Clusters stored; downstream splits group by `dup_cluster_id`.

### Thread reconstruction
- Key: `subject_norm` plus participant overlap within a time window (default 30 days).
- Use `In-Reply-To` and `References` when present.
- Assign confidence by evidence type; audit 100 messages for accuracy.
- Ambiguous generic subjects (e.g., empty or one-word) become singleton threads.

### Matching rules for extraction evaluation
- **Strict:** same field and exact character span after trimming whitespace and punctuation.
- **Lenient:** same field and token overlap F1 at least 0.5 (used for action items and as sensitivity analysis).
- **Normalized value:** for dates, resolved ISO date using the email date as the anchor; for amounts, numeric value and currency. Reported separately from span detection.
- Metrics: precision, recall, F1 per field; micro and macro averages.

### Statistics
- **Cluster bootstrap:** resample emails with replacement, recompute metrics, 10,000 replicates, percentile intervals.
- **Paired comparison:** same resample applied to both systems; difference distribution gives CI and a two-sided p-value.
- **Multiplicity:** Holm correction over the pre-specified primary comparisons.
- **Classification:** McNemar for paired accuracy comparisons where applicable; paired bootstrap for PR-AUC and macro-F1.
- **Agreement:** Cohen's kappa for category; pairwise span F1 for entities.

### Change-point detection
- Series: weekly message count, unique senders, mean recipients per message (log-transformed).
- Method: PELT with an RBF or L2 cost; penalty chosen by a BIC-like criterion and checked for stability across penalties.
- Evaluation: fraction of breakpoints within +/-4 weeks of an event in `config/events.yaml`, compared with 10,000 random-event permutations.

### Network
- Directed weighted graph: sender to each recipient, weight 1/n_recipients per message to reduce mass-mailing dominance; messages with more than K recipients (default 50) excluded in a sensitivity run.
- Metrics: in/out degree, PageRank, betweenness; Leiden communities; modularity compared with a degree-preserving randomization null.

## 5. LLM client design
- Prompt templates versioned in `config/prompts/`; version string part of cache key.
- Few-shot examples drawn from dev partition only.
- Output validated with a pydantic schema (list of spans with field, text, optional normalized value); text is aligned back to offsets deterministically; unmatched strings are counted as hallucinations.
- Retry policy: exponential backoff, maximum 3 attempts; failure flagged, not dropped.
- Cache key: SHA-256 of (model id, prompt version, text sha256).
- Budget guard: estimate tokens before the call; abort when projected spend exceeds the cap.

## 6. Error handling
Parse failures are retained with null fields; all error counts roll up into the stage lineage record and fail the gate if above configured thresholds.

## 7. Determinism
Seeds derived per component from the master seed with a stable hashing scheme; all shuffles and bootstraps use explicit `numpy.random.Generator` instances.
