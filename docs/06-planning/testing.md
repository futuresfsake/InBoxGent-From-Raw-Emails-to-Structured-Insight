# Testing Strategy

Data science fails quietly. Testing therefore covers four layers: code correctness, data validity, statistical validity and reproducibility.

## 1. Unit tests (`tests/unit`)
- **Parsing:** missing or malformed headers, odd encodings, multiple recipients, timezone offsets.
- **Cleaning:** each step on hand-written fixtures; nested quotes; forwarded chains; signatures with and without delimiters; non-English text; very short bodies.
- **Deduplication:** identical, near-identical (whitespace, small edits), and distinct pairs; canonical selection rules.
- **Threading:** reply chains, subject changes, generic subjects, cross-custodian copies.
- **Evaluator:** known prediction/gold pairs with hand-computed precision, recall and F1; strict versus lenient edge cases; empty predictions; empty gold.
- **Statistics:** bootstrap returns the expected interval on synthetic data with known parameters; paired bootstrap yields zero difference when both systems are identical; Holm correction matches reference values.
- **Agreement:** kappa and span F1 on constructed examples with known answers.
- **LLM client:** mocked API; schema validation failures; retry and backoff; cache hit and miss; budget guard stops spending.
- **Normalizers:** date resolution relative to email date; amount parsing with currencies and abbreviations.

## 2. Property-based tests (`tests/property`, hypothesis)
- Cleaning is idempotent: `clean(clean(x)) == clean(x)`.
- Cleaning never increases text length.
- Parsing round-trips normalized address lists.
- Span offsets always lie within the text and satisfy `start < end`.
- Splitting functions are deterministic given a seed.

## 3. Data validation tests (pandera, run in pipeline and CI)
- Schemas and dtypes match the LLD.
- Unique message ids; one canonical message per duplicate cluster.
- Date range plausibility; parse-failure rate under threshold.
- Null-rate thresholds per column.
- Lineage totals reconcile (rows in minus removed equals rows out).
- Gold labels: `text_sha256` matches the rebuilt text for every labeled email.

## 4. Statistical-validity and leakage tests (`tests/integration`)
- No `thread_id` appears in more than one partition.
- No `dup_cluster_id` spans partitions.
- Temporal split: maximum train timestamp is earlier than minimum test timestamp.
- Test-id hash equals the committed lock value.
- T2 features contain no post-send information (feature allowlist check).
- Historical aggregate features use only strictly earlier messages (checked on constructed timelines).
- Dev prompt examples contain no test-partition ids.

## 5. Metamorphic tests for extractors
- Adding irrelevant whitespace does not change extracted values.
- Shifting the email date shifts resolved relative dates accordingly.
- Reordering independent paragraphs does not remove entities.
- Duplicating a paragraph does not create new distinct entities after deduplication of results.

## 6. Pipeline integration test
A committed synthetic fixture (about 30 fake emails) runs through all stages in under a minute in CI. The test asserts expected row counts, gate outcomes and a snapshot of key metrics on fixture gold labels.

## 7. Manual validation
| Check | Size | Acceptance |
|---|---|---|
| Cleaning audit | 100 emails stratified by custodian | At least 90% clean; failures categorized |
| Dedup pair audit | 100 candidate pairs | Precision and recall reported; threshold justified |
| Thread audit | 100 messages | Accuracy with CI reported |
| Annotation agreement | At least 25% of gold set | Kappa 0.70+, span F1 0.80+ |
| Redaction audit | 50 published snippets or figures | Zero personal identifiers |

## 8. Reproducibility tests
- Rerun a stage twice with the same seed: outputs identical (hash comparison).
- Fresh-clone install and `make all` on the fixture succeeds in CI.
- Reported tables regenerate within tolerance at release.

## 9. Coverage and tooling
- Line coverage at least 80% on cleaning, parsing, dedup, threading, evaluate and splits modules.
- pytest, pytest-cov, hypothesis, ruff, mypy on selected modules.
- pre-commit runs lint and fast tests; CI runs the full suite.

## 10. Test data policy
Only synthetic emails and aggregate statistics are committed. Real corpus text appears only in ignored local directories.
