# High-Level Design (HLD)

## 1. Architectural style
A staged, idempotent batch pipeline over versioned Parquet artifacts, with data-quality gates between stages and a lineage record per artifact. Analysis tracks consume shared curated tables and write results to an experiment tracker.

## 2. System context

```
Public Enron corpus ----> InBoxGent pipeline ----> Findings report, model card, datasheet
Anthropic API  --------->   (local batch)    ----> Optional Streamlit dashboard
Hugging Face hub (models)
```

External dependencies are limited to dataset download, an LLM API (extraction only) and model weight downloads.

## 3. Pipeline view

```
 raw/ (manifest)
    |
 [S1 Ingest + Sample]        gate G1
    |
 [S2 Parse headers]          gate G2
    |
 [S3 Clean body]             gate G3   -> lineage log
    |
 [S4 Dedup]                  gate G4   -> duplicate clusters, canonical ids
    |
 [S5 Thread reconstruction]  gate G5   -> thread ids, audit sample
    |
    +--> clean_emails (frozen version "clean_vN")
             |
   +---------+----------------------+------------------------+
   |                                |                        |
 [Track IE]                    [Track ML]               [Track EX]
 gold set (dev/test lock)      label building (T1,T2)   EDA, topics, network,
 4 extractors                  feature building         change points, anomalies
 evaluator (CIs, tests)        splits (grouped/temporal)
 cost / latency                models, calibration,
 error taxonomy                ablations, SHAP
   |                                |                        |
   +---------------+----------------+------------------------+
                   |
        Experiment tracker (MLflow) + result tables
                   |
        [Reporting] findings.md, model_card.md, datasheet, dashboard
```

Dependencies: Track IE needs a frozen `clean_vN`. Track ML feature set F3 depends on Track IE outputs. Track EX depends only on S5 output.

## 4. Components

| Id | Component | Responsibility | Package |
|---|---|---|---|
| C1 | Ingest and sampler | Manifest, seeded stratified sampling with inclusion probabilities | `inboxgent.ingest` |
| C2 | Parser | Header parsing to typed columns | `inboxgent.parse` |
| C3 | Cleaner | Quote, forward, signature and disclaimer removal; normalization | `inboxgent.cleaning` |
| C4 | Deduplicator | Exact and MinHash/LSH near-duplicate clustering | `inboxgent.dedup` |
| C5 | Threader | Thread reconstruction and audit tooling | `inboxgent.threading` |
| C6 | Quality gates | Pandera schemas and checks | `inboxgent.quality` |
| C7 | Privacy | PII detection and redaction | `inboxgent.privacy` |
| C8 | Annotation tooling | Sampling for gold set, agreement metrics, adjudication | `inboxgent.annotation` |
| C9 | Extractors | Rules, spaCy, small LLM, larger LLM, optional cascade | `inboxgent.extract` |
| C10 | Evaluator | Matching, metrics, bootstrap, paired tests, error taxonomy | `inboxgent.evaluate` |
| C11 | Feature builder | Metadata, text, extracted-field features | `inboxgent.features` |
| C12 | Models | Baselines, boosted and embedding models, calibration | `inboxgent.models` |
| C13 | Analysis | EDA, topics, network, change points, anomalies | `inboxgent.analysis` |
| C14 | Tracking | MLflow wrapper, lineage metadata | `inboxgent.tracking` |
| C15 | Reporting | Table and figure generation, report assembly | `inboxgent.reporting` |
| C16 | Dashboard (stretch) | Interactive exploration | `app/` |

## 5. Key design decisions (see also [decision-log](decision-log.md))
1. Deduplicate before splitting and before sampling for gold, to prevent leakage and inflated metrics.
2. Annotate and evaluate extraction on a frozen cleaned text version; any cleaning change creates a new version and invalidates dependent evaluations.
3. Gold labels stored separately from text; text is regenerated from the public corpus.
4. Dev/test partition locked by hashing test ids before any tuning.
5. LLM calls isolated behind a cached, budget-capped client with schema-validated outputs.
6. Temporal and thread-grouped validation as the default for modeling.

## 6. Quality gates

| Gate | After | Checks |
|---|---|---|
| G1 | Ingest/sample | Manifest match, sample size, stratum counts, seed recorded |
| G2 | Parse | Parse-failure rate under threshold, UTC dates in range, unique message ids |
| G3 | Clean | No empty bodies above threshold, length distribution sanity, lineage totals consistent |
| G4 | Dedup | One canonical per cluster, cluster-size distribution reviewed |
| G5 | Thread | Thread coverage, singleton rate, audit accuracy estimate |

## 7. Failure modes and handling

| Failure | Handling |
|---|---|
| Malformed header or missing date | Keep row, null the field, count and report; exclude from time-based analyses |
| Cleaning over-removal | Lineage shows chars removed per step; audit sample; keep raw body |
| LLM timeout, rate limit or invalid JSON | Retry with backoff, then record failure flag; failures counted in metrics rather than silently dropped |
| Budget exceeded | Hard stop with partial results saved and spend logged |
| Gate failure | Pipeline halts, writes diagnostic report |

## 8. Non-functional design
- **Performance:** vectorized operations, chunked processing, DuckDB for heavy aggregations.
- **Scalability:** sized for tens of thousands of emails; design allows larger runs by configuration.
- **Security and privacy:** no private mail; PII redaction; secrets via environment; no email text committed.
- **Observability:** structured logs carrying run ID, stage summaries, lineage records.

## 9. Deployment
Local batch execution via Makefile and CLI. CI executes the pipeline on a synthetic fixture. The optional dashboard reads precomputed result tables only, never raw email text.

## 10. Trade-offs
- Staged artifacts cost disk space but make reruns and debugging cheap.
- Storing only labels (no text) in the repo adds a rebuild step but avoids redistributing real people's email.
- Four extraction systems expand scope but are what makes the cost-quality conclusion credible.
