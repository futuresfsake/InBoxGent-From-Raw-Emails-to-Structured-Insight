# Requirements Specification

**Priority:** M = must, S = should, C = could.
**Verification:** T = automated test, I = inspection, A = analysis, D = demonstration.
**Tracks:** DE data engineering, EX exploratory, IE information extraction, ML predictive modeling, RS reporting.

## Functional requirements

### Data engineering (DE)

| ID | Requirement | Pri | Ver |
|---|---|---|---|
| DE-01 | Acquire the Enron corpus and record a checksum manifest (file count, total size, hash) that identifies the exact data version used. | M | T |
| DE-02 | Draw a seeded, stratified sample (by custodian and year) of a configurable size; document the sampling frame and store inclusion probabilities. | M | T |
| DE-03 | Parse RFC 822 headers into typed columns (message id, UTC date, sender, To/Cc/Bcc recipients, subject, folder, custodian) and count parse failures. | M | T |
| DE-04 | Remove forwarded blocks, quoted replies, signatures and legal disclaimers from the body; retain the raw body. | M | T/I |
| DE-05 | Detect exact duplicates (content hash) and near-duplicates (MinHash/LSH); flag, never silently drop; assign a canonical message per duplicate cluster. | M | T |
| DE-06 | Reconstruct threads using normalized subject, participants, reference headers when present and a time window; report estimated thread accuracy on a manual audit. | M | I/A |
| DE-07 | Emit a lineage log per stage: rows in and out, per-step characters removed, null rates, runtime, code and config hash. | M | T |
| DE-08 | Enforce a data-quality gate (schema, ranges, uniqueness, null-rate thresholds) after every stage; fail loudly on violation. | M | T |
| DE-09 | Detect and redact PII (e.g., phone numbers, SSN-like strings, credit-card-like strings) in any artifact intended for publication. | M | T/I |

### Exploratory analysis (EX)

| ID | Requirement | Pri | Ver |
|---|---|---|---|
| EX-01 | Perform EDA covering volume over time, custodian and sender distributions, length distributions, recipient counts, missingness, and duplicate rates; record hypotheses generated. | M | I |
| EX-02 | Fit topic models on cleaned and raw text; evaluate with coherence and cross-seed stability; label topics with human-readable names. | S | A |
| EX-03 | Build a directed, weighted sender-recipient network; compute centrality and communities; compare modularity against a null model; handle mass-mailings explicitly. | S | A |
| EX-04 | Run change-point detection on weekly series; compare breaks to a pre-registered event list using a permutation baseline. | S | A |
| EX-05 | Run anomaly detection on sender-week features and review top anomalies qualitatively. | C | I |

### Information extraction (IE)

| ID | Requirement | Pri | Ver |
|---|---|---|---|
| IE-01 | Define the extraction schema and annotation guidelines (person, organization, date, amount, action item) with decision rules for edge cases. | M | I |
| IE-02 | Build a gold set (target 300 emails, floor 200) stratified by custodian and year, annotated on frozen cleaned text; double-annotate at least 25%; report agreement; split into dev and test and lock test. | M | A |
| IE-03 | Implement four extraction systems behind a common interface: rules, spaCy, small LLM, larger LLM. | M | T |
| IE-04 | LLM backend: temperature 0, schema-validated structured output, retries with backoff, response caching keyed by model + prompt version + text hash, pinned model identifiers. | M | T |
| IE-05 | Evaluate with strict and lenient matching at span level, plus normalized-value correctness for dates and amounts; report per field and micro/macro averages with cluster-bootstrap 95% CIs. | M | T |
| IE-06 | Run paired significance tests for the primary comparisons with multiplicity correction. | M | A |
| IE-07 | Measure cost per 1,000 emails, cost per true positive, latency (p50/p95) and throughput; present a cost-quality Pareto view. | M | A |
| IE-08 | Categorize errors into a taxonomy (boundary, type confusion, hallucination, missed, normalization) with counts per system. | M | A |
| IE-09 | Implement a cascaded/hybrid extractor that routes uncertain cases to an LLM and evaluate its cost-quality position. | C | A |

### Predictive modeling (ML)

| ID | Requirement | Pri | Ver |
|---|---|---|---|
| ML-01 | Define tasks T1 (category) and T2 (reply within W hours) with label provenance, exclusion rules and censoring handling; document label noise. | M | I |
| ML-02 | Use leakage-safe splits: deduplicate first, group by thread, and use a temporal holdout plus rolling-origin validation; also report a random grouped split to quantify optimism. | M | T/A |
| ML-03 | Train baselines (majority, simple heuristic, TF-IDF + logistic regression) and stronger models (gradient boosting on metadata plus features, embeddings + logistic regression). | M | T |
| ML-04 | Report PR-AUC, macro-F1, balanced accuracy, and calibration (Brier score, ECE, reliability curves) with bootstrap CIs; apply and evaluate recalibration. | M | A |
| ML-05 | Perform ablations: raw versus cleaned text, metadata only versus text only versus text plus extracted features, with and without near-duplicate removal. | M | A |
| ML-06 | Provide interpretability (coefficients, permutation importance or SHAP) and slice-based error analysis (by custodian, year, length). | S | A |
| ML-07 | Track every training run (parameters, data manifest hash, code version, metrics, artifacts) in an experiment tracker. | M | D |

### Reporting (RS)

| ID | Requirement | Pri | Ver |
|---|---|---|---|
| RS-01 | Produce a findings report with all pre-specified hypotheses resolved as supported, not supported or inconclusive. | M | I |
| RS-02 | Produce a dataset datasheet and a model card for each released model. | M | I |
| RS-03 | Provide an interactive dashboard to explore results. | C | D |
| RS-04 | Include limitations, ethics and privacy sections. | M | I |

## Non-functional requirements

| ID | Requirement | Pri | Ver |
|---|---|---|---|
| NFR-01 | Reproducibility: fixed seeds, pinned and locked dependencies, data manifest hash, identical metrics on rerun. | M | T |
| NFR-02 | Privacy: raw and intermediate email text never committed; gold set stores labels and message ids only. | M | I |
| NFR-03 | Modularity: logic in `src/inboxgent`, notebooks orchestrate and display only. | M | I |
| NFR-04 | Testability: at least 80% line coverage on cleaning, parsing, dedup, threading and evaluation modules. | S | T |
| NFR-05 | Performance: full cleaning of a 50k-email sample in under 15 minutes on a laptop. | S | T |
| NFR-06 | Cost control: configurable budget cap on LLM spend with hard stop and logged spend. | M | T |
| NFR-07 | Documentation: every notebook states its question, method, result and conclusion. | S | I |
| NFR-08 | Observability: structured logging with run ID across all stages. | S | I |
| NFR-09 | Portability: runs on Windows, macOS and Linux with documented setup. | S | D |
| NFR-10 | Secrets management: secrets only via environment variables or a git-ignored `.env`; secret fields masked in logs and config output; secret scanning in pre-commit and CI. | M | T |
| NFR-11 | Credential and access control: dedicated, spend-limited LLM API key; 2FA and least-privilege credentials for GitHub; branch protection on `main` requiring passing CI. | M | I |
| NFR-12 | Supply chain security: locked dependencies, `pip-audit` and Dependabot, CI actions with least-privilege permissions. | M | T |
| NFR-13 | Repository governance: `SECURITY.md`, `LICENSE`, `CODEOWNERS`, PR template with a data and secrets checklist. | M | I |
| NFR-14 | Threat model: documented assets, threats and mitigations, with verification tests for key controls (see [security](../03-tech/security.md)). | M | I/T |
| NFR-15 | Untrusted-input handling: email text and LLM outputs treated as untrusted; no code execution on either; LLM outputs accepted only after schema validation. | M | T |

## Constraints
- Single developer, part-time.
- No GPU assumed.
- LLM spend bounded by a budget cap.

## Assumptions
- Enron corpus remains publicly accessible.
- Labeling effort of about 300 emails and about 400 category labels is feasible.
- Thread reconstruction from headers and subjects is accurate enough after manual audit.

## Traceability
Each requirement maps to milestones in [milestones-foundation](../06-planning/milestones-foundation.md) and to user stories in [user-stories](user-stories.md).
