# Modeling Plan

Covers the predictive tasks (T1, T2, optional T3), the unsupervised analyses (U1), the network analysis (N1) and the change-point analysis (C1). Evaluation rules live in [evaluation-methodology](evaluation-methodology.md).

## 1. Task T1: Email category

### Definition
Multiclass classification of each canonical email into `business`, `personal`, `other` (automated, newsletters, system mail).

### Labels
- Hand-label about 400 stratified emails following written definitions.
- If an externally available annotated subset of the corpus is found to be usable and properly attributable, it may supplement training; it is never used for the locked test set and its label scheme is mapped explicitly (see open questions).
- Label noise handled by double-labeling 20% and reporting kappa.

### Features
- Text: TF-IDF (word and character n-grams) on `body_clean`; sentence embeddings.
- Metadata: recipient count, sender domain type (internal or external), time of day, weekday, subject length, has attachment marker text.
- Extracted fields from Track IE (counts of dates, amounts, organizations, action items) as an ablation group.

### Models
1. Majority class
2. Keyword heuristic
3. TF-IDF + logistic regression (regularization tuned)
4. Sentence embeddings + logistic regression
5. LightGBM on metadata and aggregate text features

### Specific risks
- Folder names can reveal the label (for example a personal-looking folder): excluded from features.
- Small labeled set: use repeated stratified CV in training for model selection, report test once.

## 2. Task T2: Reply within W hours

### Definition
For a message with at least one custodian recipient, predict whether a reply from a recipient appears in the same thread within W = 24 hours (sensitivity: 72 hours).

### Label construction
1. Use thread assignments from the threader; require thread confidence above a threshold.
2. A reply is a later message in the thread whose sender is among the original recipients.
3. Exclude messages within W hours of the end of the custodian's data (right-censoring).
4. Exclude automated mail and mass-mailings above a recipient threshold.

### Features (grouped for ablation)
- **F1 metadata:** recipient counts, hour/day, sender and custodian relationship statistics computed only from past data (strict time-ordered aggregation), subject patterns.
- **F2 text:** TF-IDF and embeddings of cleaned body and subject.
- **F3 extracted:** question presence, number of dates, amounts and action items from the best extraction system.

### Leakage controls
- Historical aggregates (such as sender's past reply rate) use only messages strictly before the focal message.
- No thread-level information from after the focal message.
- Duplicate clusters and threads grouped in all splits.

### Models
Majority, heuristic, logistic regression on F1, TF-IDF + LR on F2, LightGBM on F1+F2+F3, embedding + LR.

### Evaluation
PR-AUC primary; calibration; slice analysis by custodian, period and message length; comparison under temporal and random grouped splits.

## 3. Optional task T3: Action-item sentences
Sentence-level binary classification trained from gold action_item annotations. Included only if time allows; serves as a bridge between extraction and modeling and a candidate cascade router.

## 4. Interpretability
- Linear models: top coefficients with stability across CV folds.
- Boosted models: permutation importance and SHAP; check that attributions are not dominated by leakage-like features.
- Error analysis: confusion matrix, highest-confidence mistakes, slice performance.

## 5. Calibration
Reliability curves and ECE before and after isotonic or Platt scaling fit on validation data; report whether calibration holds under the temporal shift.

## 6. Experiment protocol
- Seeds: at least 5 for stochastic models; report mean and spread.
- Hyperparameter search: bounded random search on the training period; budget recorded.
- Tracking: every run logged (parameters, data manifest hash, code SHA, metrics).
- Model selection uses validation only; test evaluated once for final candidates.

## 7. Unsupervised analysis U1: Topics
- Inputs: cleaned and raw text variants (supports H3).
- Pipeline: sentence embeddings, UMAP, HDBSCAN (BERTopic); sensitivity to key parameters.
- Evaluation: coherence, cross-seed stability, redundancy, qualitative review.
- Output: named topics with representative terms, prevalence over time.

## 8. Network analysis N1
- Build the weighted directed graph from canonical, de-massed emails.
- Metrics: degree, PageRank, betweenness; Leiden communities; compare modularity to the randomized null.
- Temporal snapshots (quarterly) to observe structural change.
- Entity resolution of addresses to people limited to normalization of address forms; no external identification.

## 9. Change-point analysis C1
- Series: weekly message volume, unique senders, mean recipients per message.
- Methods: PELT and binary segmentation with penalty sensitivity.
- Alignment with the pre-registered event list; permutation baseline.
- Clearly labeled exploratory (H5).

## 10. Stretch analyses
- **Cascade extractor:** route low-confidence spaCy or small LLM cases to the larger LLM; plot the cost-quality frontier.
- **Anomaly detection:** Isolation Forest on sender-week features; qualitative review only.
- **Active learning:** compare random sampling versus uncertainty sampling for T1 labeling efficiency using simulated labeling on the labeled pool.
- **Time-to-reply modeling:** survival analysis as a richer alternative to the binary T2.

## 11. Deliverables from modeling
- Results tables (`reports/tables/`) with CIs
- Calibration and ablation figures
- Model card per final model
- Error analysis section in the findings report
