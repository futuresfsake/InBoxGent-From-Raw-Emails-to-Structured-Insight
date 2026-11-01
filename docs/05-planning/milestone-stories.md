# Milestone Stories

Work items grouped by milestone, each linked to the user stories in [user-stories.md](../02-requirements/user-stories.md). Size: S (under 2h), M (half day), L (1+ day).

## M0 Foundation
| Task | Size | Story |
|---|---|---|
| Scaffold repo folders and `.gitignore` | S | US-16 |
| Pin dependencies, create venv instructions | S | US-01 |
| Add `config.py` with seed, paths, sample size | S | US-01 |
| Set up ruff and pre-commit | S | US-16 |

## M1 Ingest & Parse
| Task | Size | Story |
|---|---|---|
| Download and unpack Enron corpus | S | US-01 |
| Implement seeded sampler | M | US-01 |
| Parse headers into columns | M | US-02 |
| Null-rate report | S | US-02 |

## M2 Cleaning
| Task | Size | Story |
|---|---|---|
| Unicode and whitespace normalization | S | US-03 |
| Forward and quote stripping | L | US-03 |
| Signature and disclaimer removal | L | US-03 |
| Exact and near-duplicate detection | M | US-04 |
| Cleaning log and stats | M | US-05 |
| Unit tests for edge cases | M | US-16 |

## M3 EDA
| Task | Size | Story |
|---|---|---|
| Volume and sender analysis | M | US-11 |
| Network graph | M | US-11 |
| Length and response-time distributions | M | US-11 |

## M4 Gold Set
| Task | Size | Story |
|---|---|---|
| Write annotation guidelines | M | US-08 |
| Select stratified sample | S | US-08 |
| Label 200 emails | L | US-08 |
| Consistency check on 20% | M | US-08 |

## M5 Extraction & Evaluation
| Task | Size | Story |
|---|---|---|
| Extractor interface and shared types | S | US-07 |
| Rules backend | M | US-06 |
| spaCy backend | M | US-06 |
| LLM backend with caching | L | US-06 |
| Evaluator with per-field metrics | M | US-09 |
| Cost and latency tracking | S | US-10 |
| Error analysis write-up | M | US-09 |

## M6 Classification
| Task | Size | Story |
|---|---|---|
| Define and label classes | M | US-12 |
| Baselines and TF-IDF model | M | US-12 |
| Embedding model and cross-validation | M | US-12 |
| Error analysis and confusion matrix | S | US-12 |

## M7 Topics
| Task | Size | Story |
|---|---|---|
| Embed and cluster | M | US-13 |
| Name and describe topics | M | US-13 |
| UMAP visualization | S | US-13 |

## M8 Polish & Publish
| Task | Size | Story |
|---|---|---|
| Findings report | L | US-14 |
| README summary with figures | M | US-14 |
| Streamlit dashboard (stretch) | L | US-15 |
| Final test and lint pass | S | US-16 |
