# Milestone Stories

Work items per milestone with traceability and dependencies.

- **Size:** S under 2 hours, M half a day, L a day or more, XL multiple days.
- **Depends on:** tasks that must be finished (or at least started, where noted) first.
- **Blocked by gap:** items in the [gap register](gap-register.md) that need a Product Owner answer before the task can start or finish.
- **Story / Req:** links to [user stories](../02-requirements/user-stories.md) and [requirements](../02-requirements/requirements-specification.md).

## Critical path
`M0-01` to `M0-08` (foundation) then `M1-01` to `M1-05` (data) then `M2-10` (frozen cleaning) then `M4-04` (annotation, the longest task) then `M4-07` (test lock) then `M5-05` and `M5-10` (extraction results) then `M6-02` feature group F3 then `M8-01` (findings report).

Any slip on annotation (`M4-04`, `M4-08`) moves the finish date directly. Tasks on other branches (M6 baselines, all of M7) can run in parallel and absorb waiting time.

---

## M0 Foundation, security and framing
**Entry criteria:** none. Gaps G-01 to G-10 should be answered before the tasks that name them.

| ID | Task | Size | Story | Req | Depends on | Blocked by gap |
|---|---|---|---|---|---|---|
| M0-01 | Repo skeleton, `.gitignore`, pyproject, lock file | S | US-33 | NFR-01 | none | |
| M0-02 | Typed config with secret masking, logging, CLI, Makefile | M | US-33 | NFR-03, NFR-10 | M0-01 | |
| M0-03 | `.env.example` and environment-only key loading | S | US-34 | NFR-10 | M0-02 | |
| M0-04 | Dedicated spend-limited API key and budget-cap skeleton | S | US-34 | NFR-06, NFR-11 | M0-03 | G-05 |
| M0-05 | pre-commit: ruff, detect-secrets, bandit, data-path and size blockers, nbstripout | M | US-08, US-34 | NFR-10 | M0-01 | |
| M0-06 | Synthetic fixture dataset | M | US-33 | NFR-04 | M0-01 | |
| M0-07 | CI workflow (lint, types, tests, audit, secret scan, fixture pipeline) | M | US-33 | NFR-04, NFR-12 | M0-02, M0-05, M0-06 | |
| M0-08 | Dependabot and `pip-audit` in CI | S | US-34 | NFR-12 | M0-07 | |
| M0-09 | `SECURITY.md`, `CODEOWNERS`, PR template, `LICENSE` | S | US-34 | NFR-13 | M0-01 | G-08, G-10 |
| M0-10 | GitHub hardening: 2FA, SSH key or fine-grained token, branch protection, required checks | S | US-34 | NFR-11 | M0-07 | G-04, G-06, G-07 |
| M0-11 | Threat model document (drafted in [security](../03-tech/security.md); review and finalize) | M | US-34 | NFR-14 | none | |
| M0-12 | Security verification tests (fake key rejected, path blocker, config masking, budget cap) | M | US-34 | NFR-14, NFR-15 | M0-02, M0-04, M0-05, M0-07 | |
| M0-13 | Lock problem framing, hypotheses and evaluation protocol (drafted; needs sign-off) | S | US-14 | RS-01 | none | G-25 |
| M0-14 | Experiment-tracking decision and skeleton | S | US-25 | ML-07 | M0-02 | G-09 |

**Exit gate:** see M0 exit criteria in [milestone-reference](milestone-reference.md).

---

## M1 Acquisition and data understanding
**Entry criteria:** M0-01, M0-02, M0-05, M0-07 done. Enough disk space for the raw corpus.

| ID | Task | Size | Story | Req | Depends on | Blocked by gap |
|---|---|---|---|---|---|---|
| M1-01 | Download corpus and build manifest | S | US-01 | DE-01 | M0-02 | |
| M1-02 | Full-corpus exact-duplicate hashing | M | US-04 | DE-05 | M1-01 | |
| M1-03 | Stratified seeded sampler with inclusion probabilities | M | US-01 | DE-02 | M1-01, M1-02 | G-11 |
| M1-04 | Header parser with failure accounting | M | US-02 | DE-03 | M1-01 (can start on fixture from M0-06) | |
| M1-05 | Pandera schemas and gates G1-G2 | M | US-07 | DE-08 | M1-03, M1-04 | |
| M1-06 | Datasheet verification pass | M | US-31 | RS-02 | M1-01 to M1-05 | G-12 |

---

## M2 Cleaning, dedup, threads, quality gates
**Entry criteria:** M1-05 done (gates G1-G2 pass).

| ID | Task | Size | Story | Req | Depends on | Blocked by gap |
|---|---|---|---|---|---|---|
| M2-01 | Normalization and forwarded-block stripping | M | US-03 | DE-04 | M1-04 | |
| M2-02 | Quoted-reply stripping | L | US-03 | DE-04 | M2-01 | |
| M2-03 | Signature and disclaimer removal, boilerplate mining | L | US-03 | DE-04 | M2-02 | |
| M2-04 | Lineage logging (build alongside M2-01) | M | US-06 | DE-07 | M2-01 | |
| M2-05 | Near-duplicate clustering and threshold selection | L | US-04 | DE-05 | M2-03 | G-13 |
| M2-06 | Thread reconstruction and audit | L | US-05 | DE-06 | M1-04, M2-05 | G-15 |
| M2-07 | PII detection and redaction utilities | M | US-08 | DE-09 | M2-03 | |
| M2-08 | Cleaning audit (100 emails) | M | US-03 | DE-04 | M2-03 | G-14 |
| M2-09 | Property-based and edge-case tests | M | US-33 | NFR-04 | M2-01 to M2-03 | |
| M2-10 | Freeze `clean_v1` (gates G3-G5 pass) | S | US-11 | IE-02 | M2-05, M2-06, M2-08 | |

---

## M3 EDA and hypothesis refinement
**Entry criteria:** `clean_v1` frozen (M2-10).

| ID | Task | Size | Story | Req | Depends on | Blocked by gap |
|---|---|---|---|---|---|---|
| M3-01 | Volume, custodian, length, recipient and missingness analysis | M | US-09 | EX-01 | M2-10 | |
| M3-02 | Mass-mail and automated-mail analysis | M | US-09 | EX-01 | M3-01 | G-16 |
| M3-03 | Duplicate and thread statistics | S | US-09 | EX-01 | M2-10 | |
| M3-04 | Decide temporal split boundaries and T2 exclusions | M | US-20 | ML-02 | M3-01 to M3-03 | G-15, G-17, G-18 |
| M3-05 | Record generated hypotheses (kept separate from pre-registered ones) | S | US-09 | EX-01 | M3-01 to M3-03 | |

---

## M4 Annotation
**Entry criteria:** M2-10 and M3-04 done; schema decisions made.

| ID | Task | Size | Story | Req | Depends on | Blocked by gap |
|---|---|---|---|---|---|---|
| M4-01 | Write annotation guidelines (entities and T1 categories) | L | US-10 | IE-01 | M2-10, M3-05 | G-20, G-21 |
| M4-02 | Pilot annotation (20 emails) and revise guidelines | M | US-10 | IE-01 | M4-01 | |
| M4-03 | Stratified gold sampling and hard-case set | M | US-11 | IE-02 | M2-10, M3-04 | G-23 |
| M4-04 | Annotate primary set | XL | US-10 | IE-02 | M4-02, M4-03 | G-23, G-02 |
| M4-05 | Second pass on at least 25% and agreement metrics | L | US-10 | IE-02 | M4-04 | G-19, G-24 |
| M4-06 | Adjudication | M | US-10 | IE-02 | M4-05 | |
| M4-07 | Dev/test assignment and hash lock | S | US-11 | IE-02 | M4-06 | G-25 |
| M4-08 | T1 category labeling (about 400) | XL | US-19 | ML-01 | M3-04, M4-01 | G-21, G-22, G-23 |

---

## M5 Extraction benchmark
**Entry criteria:** M4-07 done (test locked). Tasks M5-01 to M5-04 may start earlier because they need only the interface and the guidelines.

| ID | Task | Size | Story | Req | Depends on | Blocked by gap |
|---|---|---|---|---|---|---|
| M5-01 | Interface and shared types | S | US-12 | IE-03 | M0-02 | |
| M5-02 | Rules backend | M | US-12 | IE-03 | M5-01, M4-01 | G-20 |
| M5-03 | spaCy backend | M | US-12 | IE-03 | M5-01 | G-28 |
| M5-04 | LLM backend: schema validation, cache, budget guard | L | US-13 | IE-04, NFR-06 | M5-01, M0-04 | G-05, G-26, G-27, G-29 |
| M5-05 | Prompt development on dev partition only | L | US-13 | IE-04 | M5-04, M4-07 | |
| M5-06 | Matching and metrics (strict, lenient, normalized) | L | US-14 | IE-05 | M5-01, M4-06 | |
| M5-07 | Cluster and paired bootstrap, Holm correction | L | US-14, US-15 | IE-05, IE-06 | M5-06 | G-25 |
| M5-08 | Cost and latency instrumentation | M | US-16 | IE-07 | M5-04 | |
| M5-09 | Error taxonomy and qualitative review | L | US-17 | IE-08 | M5-02, M5-03, M5-05, M5-07 | |
| M5-10 | Pareto analysis and H1/H2 write-up | M | US-16 | IE-07 | M5-07, M5-08, M5-09 | |

---

## M6 Predictive modeling
**Entry criteria:** M2-06 (threads), M3-04 (splits), M4-08 (T1 labels). Feature group F3 additionally needs M5-10.

| ID | Task | Size | Story | Req | Depends on | Blocked by gap |
|---|---|---|---|---|---|---|
| M6-01 | T1 and T2 label builders with exclusions and censoring | L | US-19 | ML-01 | M2-06, M3-04, M4-08 | G-18, G-21 |
| M6-02 | Feature groups F1, F2, F3 | L | US-23 | ML-03 | M6-01; F3 needs M5-10 | |
| M6-03 | Split utilities and leakage tests | L | US-20 | ML-02 | M2-06, M3-04 | G-17 |
| M6-04 | Baselines | M | US-21 | ML-03 | M6-01, M6-03, M0-14 | |
| M6-05 | TF-IDF and embedding models | M | US-21 | ML-03 | M6-04 | |
| M6-06 | LightGBM and bounded hyperparameter search | M | US-21 | ML-03 | M6-04 | |
| M6-07 | Metrics, CIs and calibration | L | US-22 | ML-04 | M6-05, M6-06 | |
| M6-08 | Ablations | L | US-23 | ML-05 | M6-07, M6-02 | |
| M6-09 | Interpretability and slice analysis | M | US-24 | ML-06 | M6-07 | |
| M6-10 | MLflow integration and run-ID reporting | M | US-25 | ML-07 | M0-14 | G-09 |

---

## M7 Topics, network and temporal analysis (Extended)
**Entry criteria:** M2-10 done. Independent of M4 and M5, so it can fill waiting time during annotation.

| ID | Task | Size | Story | Req | Depends on | Blocked by gap |
|---|---|---|---|---|---|---|
| M7-01 | Topic modeling on raw versus cleaned text | L | US-26 | EX-02 | M2-10 | |
| M7-02 | Coherence and stability evaluation | M | US-26 | EX-02 | M7-01 | |
| M7-03 | Graph construction and metrics | M | US-27 | EX-03 | M2-10 | G-15, G-16 |
| M7-04 | Null-model comparison | M | US-27 | EX-03 | M7-03 | |
| M7-05 | Event list and change-point detection | M | US-28 | EX-04 | M3-01 | G-31 |
| M7-06 | Permutation baseline and sensitivity | M | US-28 | EX-04 | M7-05 | |

---

## M8 Synthesis and release
**Entry criteria:** all Core results available; reproducibility and ethics checklists open.

| ID | Task | Size | Story | Req | Depends on | Blocked by gap |
|---|---|---|---|---|---|---|
| M8-01 | Findings report | XL | US-30 | RS-01 | M5-10, M6-09, (M7-06 if built) | |
| M8-02 | Model cards and datasheet | M | US-31 | RS-02 | M6-09, M1-06 | |
| M8-03 | Limitations and ethics sections | M | US-31 | RS-04 | M8-01 | |
| M8-04 | README headline results | M | US-30 | RS-01 | M8-01 | G-03 |
| M8-05 | Reproducibility fresh-clone test | M | US-33 | NFR-01 | all Core tasks | |
| M8-06 | Release tag, changelog, citation check | S | US-33 | NFR-01 | M8-02, M8-03, M8-05 | G-04, G-34 |

---

## Stretch

| ID | Task | Size | Story | Req | Depends on | Blocked by gap |
|---|---|---|---|---|---|---|
| S-01 | Cascade extractor | L | US-18 | IE-09 | M5-10 | G-32 |
| S-02 | Anomaly detection | M | US-29 | EX-05 | M2-10 | G-32 |
| S-03 | Active learning simulation | L | | | M4-08 | G-32 |
| S-04 | Streamlit dashboard | L | US-32 | RS-03 | M8-01 | G-32, G-33 |

## Parallelism guide

| While waiting on... | Work on... |
|---|---|
| Annotation (M4-04, M4-08) | M7 (all), M6-03 split utilities, M6-10 tracking, M5-01 to M5-04 backends |
| Gap answers G-05, G-26 (LLM) | M5-02, M5-03 rules and spaCy backends |
| M5 completion | M6-04 to M6-07 with feature groups F1 and F2 |
