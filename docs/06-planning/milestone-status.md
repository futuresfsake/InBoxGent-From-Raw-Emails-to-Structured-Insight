# Milestone Status

**Last updated:** 2026-11-08

Legend: Not started, In progress, Blocked, Done

## Dashboard

| ID | Milestone | Tier | Status | Progress | Notes |
|---|---|---|---|---|---|
| M0 | Foundation and framing | Core | In progress | Design docs, hypotheses and evaluation protocol written | Code done: M0-01 (no lock file), M0-02, M0-03, M0-05, M0-06, M0-07 (CI unverified), M0-08, M0-09 (files; contact is GitHub issues), M0-12 (tests), M0-14 (MLflow skeleton), M0-04 (in-code cap). Gaps defaulted 2026-11-08. Remaining for Product Owner: provider spend limit, GitHub 2FA and SSH key, branch protection (M0-10), confirm CI is green |
| M1 | Acquisition and data understanding | Core | In progress | Fixture-level code: manifest, exact dedup, header parser, stratified sampler (30k default), gates G1-G2 (pure Python, not pandera) | Remaining: real corpus download and profiling, datasheet verification (G-12) |
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

## Blockers and dependencies
No task is blocked by work yet. Pending Product Owner answers that gate upcoming tasks (full mapping in [milestone-stories](milestone-stories.md) and the [gap register](gap-register.md)):

| Upcoming task | Blocked by gap |
|---|---|
| M0-04 spend-limited API key | G-05 |
| M0-09 license, SECURITY.md | G-08, G-10 |
| M0-10 GitHub hardening | G-04, G-06, G-07 |
| M0-13 lock hypotheses | G-25 |
| M0-14 tracking skeleton | G-09 |
| M1-03 sampler | G-11 |

Critical path: M0 foundation, M1 data, M2-10 frozen cleaning, M4-04 annotation, M4-07 test lock, M5 results, M6 feature group F3, M8 report.

## Risk watch
Top current risks: annotation effort (R-03), scope creep (R-01), cleaning heuristics quality (R-02).

## Change log

| Date | Change |
|---|---|
| 2026-11-01 | Initial planning docs created. |
| 2026-11-01 | Planning restructured around data science methodology: hypotheses, evaluation protocol, modeling plan, ethics, reproducibility, expanded scope tiers. |
| 2026-11-01 | M0 broadened to include security and access management: threat model, secrets handling, supply chain, repo governance (NFR-10 to NFR-15, US-34). |
| 2026-11-08 | Implementation started: package skeleton, typed config with secret masking, logging redaction, CLI, Makefile, pre-commit and .githooks, data-path blocker, CI workflow, unit tests. |
| 2026-11-08 | Added fixture dataset, Dependabot, manifest, header parser and exact dedup (fixture-level). |
| 2026-11-08 | Gap defaults accepted. Added LICENSE, SECURITY.md, CODEOWNERS, PR template, budget guard, tracking skeleton, sampler and gates G1-G2. |
