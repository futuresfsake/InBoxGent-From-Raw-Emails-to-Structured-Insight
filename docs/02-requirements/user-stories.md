# User Stories

## Personas
- **Analyst (author):** builds, runs and documents the study.
- **Skeptical reviewer:** a senior data scientist who probes methodology, leakage and statistics.
- **Hiring manager:** wants a fast, credible read of what was done and what it shows.
- **Researcher / reuser:** wants to reuse cleaning, evaluation or extraction code.

## Stories

| ID | As a... | I want... | So that... | Reqs |
|---|---|---|---|---|
| US-01 | Analyst | a reproducible, stratified sample with a recorded data manifest | every run starts from known, versioned data | DE-01, DE-02, NFR-01 |
| US-02 | Analyst | headers parsed into typed columns with failure counts | I can trust and analyze sender, recipient and time | DE-03 |
| US-03 | Analyst | quotes, forwards, signatures and disclaimers removed | text contains only new content | DE-04 |
| US-04 | Analyst | exact and near duplicates flagged with a canonical message | counts and splits are not inflated | DE-05 |
| US-05 | Analyst | reconstructed threads with a measured accuracy | I can group splits and model reply behavior | DE-06 |
| US-06 | Analyst | a lineage log for every stage | I can justify each cleaning decision | DE-07 |
| US-07 | Analyst | automated data-quality gates | silent data corruption is caught early | DE-08 |
| US-08 | Analyst | PII redacted from anything published | the project respects privacy | DE-09, NFR-02 |
| US-09 | Analyst | exploratory analysis that records generated hypotheses | exploration is separated from confirmation | EX-01 |
| US-10 | Analyst | written annotation guidelines and a measured agreement score | labels are consistent and defensible | IE-01, IE-02 |
| US-11 | Analyst | a gold set split into dev and locked test | tuning cannot contaminate evaluation | IE-02 |
| US-12 | Analyst | interchangeable extraction systems behind one interface | comparisons are fair and new systems are cheap to add | IE-03 |
| US-13 | Analyst | LLM extraction with validated structured output, caching and pinned models | results are reproducible and cost-controlled | IE-04, NFR-06 |
| US-14 | Skeptical reviewer | per-field metrics with bootstrap confidence intervals | I can judge whether differences are real | IE-05 |
| US-15 | Skeptical reviewer | paired significance tests with multiplicity correction | I can trust headline comparisons | IE-06 |
| US-16 | Hiring manager | a cost-quality trade-off view | I see practical, business-aware judgment | IE-07 |
| US-17 | Analyst | an error taxonomy per system | I can explain why systems fail, not just that they do | IE-08 |
| US-18 | Analyst | a cascaded extractor that routes hard cases to an LLM | I can show a better cost-quality point | IE-09 |
| US-19 | Analyst | clearly defined prediction tasks with documented label provenance | models answer a well-posed question | ML-01 |
| US-20 | Skeptical reviewer | grouped and temporal splits plus a random-split comparison | I can see leakage and optimism quantified | ML-02 |
| US-21 | Analyst | baselines next to stronger models | improvement is measured against something meaningful | ML-03 |
| US-22 | Skeptical reviewer | PR-AUC, macro-F1 and calibration with CIs | model quality is judged beyond accuracy | ML-04 |
| US-23 | Analyst | ablations on cleaning and feature groups | I can attribute gains to specific choices | ML-05 |
| US-24 | Analyst | interpretability and slice-based error analysis | I can explain and stress-test models | ML-06 |
| US-25 | Analyst | tracked experiments linked to data and code versions | any result can be reproduced from its run ID | ML-07 |
| US-26 | Analyst | stable, named topics | I can summarize corpus themes credibly | EX-02 |
| US-27 | Analyst | a network analysis compared with a null model | structural claims are statistically grounded | EX-03 |
| US-28 | Analyst | change-point detection aligned with a pre-registered event list | temporal claims are not post-hoc storytelling | EX-04 |
| US-29 | Analyst | anomaly detection on sender behavior | I can surface unusual patterns for review | EX-05 |
| US-30 | Hiring manager | a README findings summary | I can judge the project in five minutes | RS-01 |
| US-31 | Skeptical reviewer | a datasheet and model card | provenance, limits and intended use are explicit | RS-02, RS-04 |
| US-32 | Hiring manager | an interactive dashboard | I can explore results without running code | RS-03 |
| US-33 | Researcher | tested, modular code | I can reuse cleaning and evaluation components | NFR-03, NFR-04 |
| US-34 | Analyst | secrets, access and dependencies managed securely, with a documented threat model | the project cannot leak keys or data, and spend and changes are controlled | NFR-10 to NFR-15 |

## Acceptance criteria (selected)

- **US-03:** On a manual audit of 100 cleaned emails stratified by custodian, at least 90% contain no residual signature or quoted-reply text; the failures are categorized.
- **US-04:** On a labeled sample of 100 duplicate-candidate pairs, the dedup rule reports precision and recall; threshold chosen on that sample.
- **US-05:** Thread assignment accuracy estimated on 100 audited messages with a stated confidence interval.
- **US-10:** Cohen's kappa at least 0.70 for category labels; pairwise span F1 at least 0.80 for entities; otherwise guidelines are revised and the double-annotated subset re-labeled.
- **US-11:** The test partition's message ids are hashed and the hash committed before any tuning; no commit after that touches test labels.
- **US-14:** Every metric in the findings report is shown with a 95% CI and the number of emails and items behind it.
- **US-20:** Assertion tests prove that no thread id appears in both train and test, no duplicate cluster spans splits, and the maximum training timestamp precedes the minimum test timestamp for temporal splits.
- **US-22:** Calibration plot and ECE are shown for the final model before and after recalibration.
- **US-25:** Any figure in the report has a run ID that resolves to parameters, data manifest hash and git SHA.
