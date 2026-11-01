# Problem Framing and Hypotheses

This document is written before any test data is examined. Changes after test evaluation must be recorded in the amendment log at the bottom.

## 1. Research questions

| ID | Question |
|---|---|
| RQ1 | How reliably can raw email be converted into clean, deduplicated, thread-aware structured data, and how much does cleaning matter downstream? |
| RQ2 | Which extraction approach gives the best accuracy per dollar for people, organizations, dates, amounts and action items? |
| RQ3 | Can email category and reply behavior be predicted under temporal and grouped validation, and do extracted fields add predictive value? |
| RQ4 | What themes, network structure and structural breaks does the corpus reveal, and do they align with known external events? |

## 2. Analytical task formulation

| Task | Type | Unit | Target | Evaluation unit |
|---|---|---|---|---|
| Cleaning | Data engineering | email | body with only new content | email (manual audit) |
| T-IE | Information extraction (sequence labeling and normalization) | email | entity and field set per email | span and normalized value |
| T1 | Multiclass classification | email | category: business, personal, other | email |
| T2 | Binary classification | (message, thread) | reply observed within W hours (W = 24 baseline, 72 sensitivity) | message |
| T3 (stretch) | Sentence classification | sentence | contains action item | sentence |
| U1 | Unsupervised | email | topics / clusters | topic quality and stability |
| N1 | Network analysis | sender-recipient pairs | graph structure over time | graph metrics versus null model |
| C1 | Change-point detection | weekly time series | break dates | alignment with event list |

## 3. Pre-specified hypotheses

Each hypothesis states the metric, the comparison and the decision rule. Confirmatory hypotheses (H1-H4) form the primary family. H5 is exploratory.

### H1: LLM extraction advantage on structured fields
**Claim:** On the locked test set, the larger LLM achieves higher strict F1 than both spaCy and rules for `date`, `amount` and `action_item`. For `person` and `organization`, spaCy is within a practical-equivalence margin of 5 F1 points of the LLM.
**Metric:** strict span-level F1 per field, cluster bootstrap by email, 10,000 resamples.
**Decision rule:** advantage supported if the 95% CI of the paired difference excludes 0 in favor of the LLM; equivalence supported if the CI lies within +/-5 points. Holm correction across the primary comparisons.
**Falsified if:** spaCy or rules match the LLM within the margin on date, amount or action_item.

### H2: Cost-quality trade-off
**Claim:** The small LLM reaches at least 90% of the larger LLM's macro-F1 at no more than 25% of the cost per 1,000 emails, and the cost per correctly extracted item of LLM systems is at least 10 times that of spaCy.
**Metric:** macro-F1 ratio; cost per 1,000 emails; cost per true positive; latency p50 and p95.
**Decision rule:** descriptive thresholds with bootstrap CIs on the ratios.

### H3: Cleaning matters downstream
**Claim:** Cleaned bodies improve macro-F1 on T1 and reduce topic redundancy compared with raw bodies, holding model and split constant.
**Metric:** paired difference in macro-F1 (bootstrap on emails); topic coherence and duplicate-topic rate for U1.
**Decision rule:** 95% CI on the macro-F1 difference excludes 0 in favor of cleaned input.
**Falsified if:** no measurable improvement; this is reported as a finding about cleaning cost-benefit.

### H4: Extracted fields add predictive value for reply behavior
**Claim:** Adding extracted structured features (question presence, dates, amounts, action-item count) to metadata and text features improves PR-AUC on T2 under a temporal split, compared with metadata-only and text-only models.
**Metric:** PR-AUC, paired bootstrap on messages grouped by thread.
**Decision rule:** improvement over the best text-only model has a 95% CI excluding 0. Minimum meaningful effect: +0.01 PR-AUC.
**Falsified if:** no improvement; extracted features are then reported as not useful for this task.

### H5 (exploratory): Structural breaks align with external events
**Claim:** Change-point detection on weekly volume, unique senders and mean recipients per message finds breaks near publicly documented events in 2001 (executive departures, earnings restatement, bankruptcy filing).
**Metric:** fraction of detected breakpoints within +/-4 weeks of an event, compared with a permutation baseline of randomly placed events.
**Decision rule:** reported with a permutation p-value; labeled exploratory and not corrected into the primary family.
**Caveat:** event list is fixed before running detection to prevent post-hoc fitting.

## 4. Analysis plan

1. Freeze cleaning pipeline version; record data manifest hash.
2. Split gold set into dev and test; lock the test partition (hash recorded in repo).
3. Tune rules, prompts and models on dev only.
4. Run all systems on test once per final configuration; log run IDs.
5. Compute metrics with cluster bootstrap CIs; run paired tests for primary comparisons; apply Holm correction.
6. Run sensitivity analyses: lenient matching, W = 72h, alternative dedup threshold.
7. Report all pre-specified results, including negative ones.

## 5. Threats to validity

| Type | Threat | Response |
|---|---|---|
| Internal | Label noise and annotator bias | Written guidelines, double annotation, adjudication, kappa |
| Internal | Dev/test contamination via prompt tuning | Few-shot examples from dev only; test locked |
| Internal | Leakage via duplicates or shared threads | Dedup before splitting; group-aware splits |
| Construct | Reply within W hours is a proxy for responsiveness, not importance | State clearly; sensitivity analysis on W |
| Construct | Reply labels missing when responder not in corpus | Restrict T2 to messages with at least one custodian recipient |
| External | Enron email from 1998-2002 may not generalize to modern email | State limitation; frame as method demonstration |
| Statistical | Small gold set gives wide CIs | Report CIs; call small differences inconclusive |
| Statistical | Multiple comparisons | Pre-specified primary family; Holm correction; exploratory results labeled |

## 6. Amendment log

| Date | Change | Reason |
|---|---|---|
| 2026-11-01 | Initial version | Project design |
