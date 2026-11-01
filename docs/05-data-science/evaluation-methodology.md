# Evaluation Methodology

The rules by which every number in this project is produced. Written before results exist.

## 1. Principles
1. Hypotheses, metrics and decision rules are pre-specified ([problem framing](../01-overview/problem-framing.md)).
2. Tune on dev, report on a locked test set, once per final configuration.
3. Every point estimate carries an uncertainty interval.
4. Compare systems on the same data with paired methods.
5. Leakage is treated as a first-class bug with automated tests.
6. Negative and inconclusive results are reported.

## 2. Gold set construction and annotation quality

### Sampling
Stratified random sample (custodian x year) at natural prevalence, plus a separately reported hard-case set.

### Partitioning
- Target 300 emails: about 100 dev, about 200 test (floor 200: about 70 dev, 130 test).
- Partition assigned by seeded hash of message id; test ids hashed (SHA-256 of sorted ids) and committed before tuning.

### Annotation process
1. Draft guidelines with definitions, examples, boundary rules, and decisions for hard cases (see IE-01).
2. Pilot on 20 emails; revise guidelines.
3. Annotator A labels all; annotator B independently labels at least 25%, mixed across dev and test.
4. Compute agreement; adjudicate disagreements; record rules created during adjudication.
5. If agreement is below target, revise guidelines and re-annotate the double-labeled subset.

If a second human annotator is unavailable, a documented substitute is used: re-annotation by the same annotator after a delay of at least two weeks (intra-annotator agreement), with the limitation stated. See open questions.

### Agreement metrics
- Category labels: Cohen's kappa (target at least 0.70).
- Entity spans: pairwise F1 between annotators under strict and lenient matching (target at least 0.80 strict).
- Normalized values (dates, amounts): exact agreement rate.

### Label hygiene
- Annotated on frozen `clean_version` text; `text_sha256` stored with labels.
- Pre-annotation by any system is prohibited, to avoid anchoring.

## 3. Extraction evaluation

### Matching
- **Strict:** exact span after whitespace and punctuation trimming, same field.
- **Lenient:** token-level overlap F1 at least 0.5.
- **Normalized:** dates resolved against the email date; amounts as value + currency. Reported separately from span detection.

### Metrics
Precision, recall, F1 per field; micro-average (item-weighted) and macro-average (field-weighted).

### Uncertainty
Cluster bootstrap over emails (items within an email are correlated), 10,000 resamples, percentile 95% intervals. With about 200 test emails, a field-level F1 near 0.8 has an email-level uncertainty of several points; fields with few items will have wide intervals and are flagged.

### Paired comparison
For each primary comparison, resample emails once per replicate and evaluate both systems on that same resample; use the distribution of differences for CI and p-value.

### Primary family and multiplicity
Primary comparisons (H1): LLM-large versus spaCy and versus rules for date, amount, action_item (6 comparisons), plus equivalence tests for person and organization (2 comparisons). Holm correction across this family. All other comparisons are exploratory and labeled so.

### Cost and latency
- Token counts and price at the time of run, recorded per run.
- Cost per 1,000 emails, cost per true positive, latency p50 and p95, and throughput.
- Cost-quality Pareto frontier plot with bootstrap bands.

### Error analysis
Taxonomy: boundary error, type confusion, spurious (hallucinated) item, missed item, normalization error, format failure. Counted per system and field; a sample of 30 errors per system reviewed qualitatively.

## 4. Classification evaluation (T1, T2)

### Splits
- **Primary:** temporal holdout: train on earliest period, validation on the middle, test on the latest period, with boundaries set by date quantiles and fixed in advance.
- **Within-training:** rolling-origin cross-validation, grouped by thread and duplicate cluster.
- **Comparison:** random grouped split reported as the optimistic reference.
- **Leakage tests (automated):**
  - No thread id in more than one partition.
  - No duplicate cluster spans partitions.
  - Max train timestamp is earlier than min test timestamp for temporal splits.
  - No feature derived from the label or from post-send information (for example reply counts) enters T2 features.

### Metrics
- Imbalance-aware: PR-AUC (primary for T2), macro-F1 and balanced accuracy (primary for T1).
- Threshold-dependent metrics reported at a threshold chosen on validation only.
- Calibration: Brier score, expected calibration error (equal-mass bins), reliability curves; recalibration (isotonic or Platt) fit on validation only.

### Uncertainty and comparison
- Bootstrap over threads (not messages) for CIs.
- Paired bootstrap for model differences; McNemar where only hard labels are compared.
- Minimum meaningful effect declared in advance (H4: +0.01 PR-AUC).

### Baselines (always reported)
Majority class; simple heuristic (for T2: sent-to-single-recipient and contains-a-question rule); TF-IDF + logistic regression.

### Ablation design
| Factor | Levels |
|---|---|
| Text source | raw body, cleaned body |
| Feature groups | metadata only, text only, text + metadata, text + metadata + extracted fields |
| Dedup | with near-duplicate removal, without |
| Representation | TF-IDF, sentence embeddings |

Each ablation changes one factor with all else fixed, using the same splits and seeds.

### Hyperparameter tuning
Performed using validation folds from the training period only; the test period is evaluated once. Search budgets are reported to bound the forking-paths risk.

## 5. Unsupervised evaluation
- **Topics:** NPMI or c_v coherence; stability via repeated runs with different seeds (topic matching by top-word overlap); duplicate-topic rate; manual labeling of topics with a short rationale.
- **Clusters:** silhouette is reported with caution for high-dimensional text; stability and interpretability prioritized.

## 6. Network and temporal evaluation
- **Network:** compare modularity and centralization with a degree-preserving randomized null (at least 1,000 randomizations); sensitivity to mass-mail threshold.
- **Change points:** pre-registered event list; metric is the fraction of breakpoints within +/-4 weeks of an event; permutation test against randomly placed events; sensitivity to penalty and series choice. Exploratory status stated in any narrative.

## 7. Reporting standards
- Tables include n (emails and items), metric, point estimate and 95% CI.
- Each figure and table cites a run ID.
- Forbidden: reporting only the best of many runs, dropping failed LLM calls from denominators, comparing systems on different data.
- A "what did not work" section is mandatory in the findings report.

## 8. Sanity checks before trusting a result
- Does a trivial baseline beat the model? Investigate leakage.
- Does performance collapse under temporal split? Report as distribution shift.
- Are results stable across seeds? Report variance.
- Do gains persist when near-duplicates are removed?
