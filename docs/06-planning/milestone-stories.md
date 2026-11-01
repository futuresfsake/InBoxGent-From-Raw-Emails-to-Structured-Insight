# Milestone Stories

Work items per milestone, linked to user stories and requirements. Size: S under 2 hours, M half a day, L a day or more, XL multiple days.

## M0 Foundation and framing
| Task | Size | Story | Req |
|---|---|---|---|
| Repo skeleton, `.gitignore`, pyproject, lock file | S | US-33 | NFR-01 |
| Typed config, logging, CLI, Makefile | M | US-33 | NFR-03 |
| pre-commit with ruff, secret scan, data-path blockers, nbstripout | S | US-08 | NFR-10 |
| CI workflow (lint, tests, fixture pipeline) | M | US-33 | NFR-04 |
| Synthetic fixture dataset | M | US-33 | NFR-04 |
| Lock problem framing and evaluation protocol | S | US-14 | RS-01 |

## M1 Acquisition and data understanding
| Task | Size | Story | Req |
|---|---|---|---|
| Download corpus and build manifest | S | US-01 | DE-01 |
| Full-corpus exact-duplicate hashing | M | US-04 | DE-05 |
| Stratified seeded sampler with inclusion probabilities | M | US-01 | DE-02 |
| Header parser with failure accounting | M | US-02 | DE-03 |
| Pandera schema and gates G1-G2 | M | US-07 | DE-08 |
| Datasheet verification pass | M | US-31 | RS-02 |

## M2 Cleaning, dedup, threads, quality gates
| Task | Size | Story | Req |
|---|---|---|---|
| Normalization and forward stripping | M | US-03 | DE-04 |
| Quote stripping | L | US-03 | DE-04 |
| Signature and disclaimer removal, boilerplate mining | L | US-03 | DE-04 |
| Lineage logging | M | US-06 | DE-07 |
| Near-duplicate clustering and threshold selection | L | US-04 | DE-05 |
| Thread reconstruction and audit | L | US-05 | DE-06 |
| PII detection and redaction | M | US-08 | DE-09 |
| Cleaning audit (100 emails) | M | US-03 | DE-04 |
| Property-based and edge-case tests | M | US-33 | NFR-04 |
| Freeze `clean_v1` | S | US-11 | IE-02 |

## M3 EDA and hypothesis refinement
| Task | Size | Story | Req |
|---|---|---|---|
| Volume, custodian, length, recipients, missingness | M | US-09 | EX-01 |
| Mass-mail and automated-mail analysis | M | US-09 | EX-01 |
| Duplicate and thread statistics | S | US-09 | EX-01 |
| Decide temporal split boundaries and T2 exclusions | M | US-20 | ML-02 |
| Record generated hypotheses | S | US-09 | EX-01 |

## M4 Annotation
| Task | Size | Story | Req |
|---|---|---|---|
| Write annotation guidelines | L | US-10 | IE-01 |
| Pilot annotation (20 emails) and revise | M | US-10 | IE-01 |
| Stratified gold sampling and hard-case set | M | US-11 | IE-02 |
| Annotate primary set | XL | US-10 | IE-02 |
| Second pass on at least 25% and agreement metrics | L | US-10 | IE-02 |
| Adjudication | M | US-10 | IE-02 |
| Dev/test assignment and hash lock | S | US-11 | IE-02 |
| T1 category labeling (about 400) | XL | US-19 | ML-01 |

## M5 Extraction benchmark
| Task | Size | Story | Req |
|---|---|---|---|
| Interface and shared types | S | US-12 | IE-03 |
| Rules backend | M | US-12 | IE-03 |
| spaCy backend | M | US-12 | IE-03 |
| LLM backend with schema validation, cache, budget guard | L | US-13 | IE-04, NFR-06 |
| Prompt development on dev | L | US-13 | IE-04 |
| Matching and metrics | L | US-14 | IE-05 |
| Cluster and paired bootstrap, Holm correction | L | US-14, US-15 | IE-05, IE-06 |
| Cost and latency instrumentation | M | US-16 | IE-07 |
| Error taxonomy and qualitative review | L | US-17 | IE-08 |
| Pareto analysis and write-up of H1/H2 | M | US-16 | IE-07 |

## M6 Predictive modeling
| Task | Size | Story | Req |
|---|---|---|---|
| T1 and T2 label builders with exclusions | L | US-19 | ML-01 |
| Feature groups F1-F3 | L | US-23 | ML-03 |
| Split utilities and leakage tests | L | US-20 | ML-02 |
| Baselines | M | US-21 | ML-03 |
| TF-IDF and embedding models | M | US-21 | ML-03 |
| LightGBM and bounded search | M | US-21 | ML-03 |
| Metrics, CIs and calibration | L | US-22 | ML-04 |
| Ablations | L | US-23 | ML-05 |
| Interpretability and slice analysis | M | US-24 | ML-06 |
| MLflow integration | M | US-25 | ML-07 |

## M7 Topics, network and temporal analysis
| Task | Size | Story | Req |
|---|---|---|---|
| Topic modeling on raw versus cleaned | L | US-26 | EX-02 |
| Coherence and stability evaluation | M | US-26 | EX-02 |
| Graph construction and metrics | M | US-27 | EX-03 |
| Null-model comparison | M | US-27 | EX-03 |
| Event list and change-point detection | M | US-28 | EX-04 |
| Permutation baseline and sensitivity | M | US-28 | EX-04 |

## M8 Synthesis and release
| Task | Size | Story | Req |
|---|---|---|---|
| Findings report | XL | US-30 | RS-01 |
| Model cards and datasheet | M | US-31 | RS-02 |
| Limitations and ethics sections | M | US-31 | RS-04 |
| README headline results | M | US-30 | RS-01 |
| Reproducibility fresh-clone test | M | US-33 | NFR-01 |
| Release tag and changelog | S | US-33 | NFR-01 |

## Stretch
| Task | Size | Story | Req |
|---|---|---|---|
| Cascade extractor | L | US-18 | IE-09 |
| Anomaly detection | M | US-29 | EX-05 |
| Active learning simulation | L | | |
| Streamlit dashboard | L | US-32 | RS-03 |
