# Milestone Status

**Last updated:** 2026-11-01

Legend: Not started, In progress, Blocked, Done

## Dashboard

| ID | Milestone | Tier | Status | Progress | Notes |
|---|---|---|---|---|---|
| M0 | Foundation and framing | Core | In progress | Design docs, hypotheses and evaluation protocol written | Remaining: repo skeleton, environment, CI, config |
| M1 | Acquisition and data understanding | Core | Not started | 0% | |
| M2 | Cleaning, dedup, threads, quality gates | Core | Not started | 0% | |
| M3 | EDA and hypothesis refinement | Core | Not started | 0% | |
| M4 | Annotation | Core | Not started | 0% | Needs decision on second annotator |
| M5 | Extraction benchmark | Core | Not started | 0% | Needs API budget decision |
| M6 | Predictive modeling | Core | Not started | 0% | |
| M7 | Topics, network, temporal | Extended | Not started | 0% | |
| M8 | Synthesis and release | Core | Not started | 0% | |
| Stretch | Hybrid, anomaly, active learning, dashboard | Stretch | Not started | 0% | |

## Current focus
Complete M0 (foundation, security and framing): repository skeleton, `.gitignore`, environment and lock file, typed configuration with secret masking, secrets and access management, pre-commit security hooks, branch protection, `SECURITY.md`, threat model, CI with audit and secret scan, synthetic fixture dataset.

## Hypothesis register

| ID | Statement (short) | Status |
|---|---|---|
| H1 | LLM beats spaCy and rules on date, amount, action_item; spaCy equivalent on person and org | Pre-registered, untested |
| H2 | Small LLM reaches 90% of large LLM quality at 25% of cost | Pre-registered, untested |
| H3 | Cleaning improves T1 and topic quality | Pre-registered, untested |
| H4 | Extracted fields improve T2 PR-AUC | Pre-registered, untested |
| H5 | Change points align with 2001 events (exploratory) | Pre-registered, untested |

## Decisions pending
See [open-questions](open-questions.md): sample size, second annotator, API budget, external labels.

## Blockers
None.

## Risk watch
Top current risks: annotation effort (R-03), scope creep (R-01), cleaning heuristics quality (R-02).

## Change log

| Date | Change |
|---|---|
| 2026-11-01 | Initial planning docs created. |
| 2026-11-01 | Planning restructured around data science methodology: hypotheses, evaluation protocol, modeling plan, ethics, reproducibility, expanded scope tiers. |
| 2026-11-01 | M0 broadened to include security and access management: threat model, secrets handling, supply chain, repo governance (NFR-10 to NFR-15, US-34). |
