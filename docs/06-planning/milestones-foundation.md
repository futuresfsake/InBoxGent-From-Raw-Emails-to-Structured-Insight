# Milestones Foundation

How work is organized, sequenced and judged complete.

## Principles
1. Each milestone yields a demonstrable, reviewable artifact, not just code.
2. Statistical and methodological safeguards are built into milestones, not added at the end.
3. Gates between milestones prevent expensive rework (for example, freezing cleaning before annotation).
4. The project is presentable at defined checkpoints even if later work is cut.

## Milestones

| ID | Name | Outcome | Requirements | Stories |
|---|---|---|---|---|
| M0 | Foundation, security and framing | Repo skeleton, environment, config, secrets and access management, supply-chain and repo governance, threat model, CI, locked hypotheses and evaluation protocol | NFR-01, NFR-03, NFR-10 to NFR-15 | US-33, US-34 |
| M1 | Acquisition and data understanding | Manifest, seeded stratified sample, parsed headers, first datasheet profile | DE-01, DE-02, DE-03 | US-01, US-02 |
| M2 | Cleaning, dedup, threads, quality gates | Frozen `clean_v1`, duplicate clusters, thread ids, lineage, PII scan | DE-04 to DE-09 | US-03 to US-08 |
| M3 | EDA and hypothesis refinement | Profiling report, documented generated hypotheses, split boundaries fixed | EX-01 | US-09 |
| M4 | Annotation | Guidelines, gold set with agreement, dev/test lock | IE-01, IE-02 | US-10, US-11 |
| M5 | Extraction benchmark | Four systems evaluated with CIs, tests, cost, error taxonomy | IE-03 to IE-08 | US-12 to US-17 |
| M6 | Predictive modeling | T1 and T2 with baselines, ablations, calibration, interpretability, tracking | ML-01 to ML-07 | US-19 to US-25 |
| M7 | Topics, network and temporal analysis | Stable topics, network results vs null, change points vs events | EX-02 to EX-04 | US-26 to US-28 |
| M8 | Synthesis and release | Findings report, model card, datasheet, README summary, release tag | RS-01, RS-02, RS-04 | US-30, US-31 |
| Stretch | Hybrid extractor, anomaly, active learning, dashboard | | IE-09, EX-05, RS-03 | US-18, US-29, US-32 |

## Dependencies

```
M0 -> M1 -> M2 -> M3 -> M4 -> M5 ----+
                  |                   +--> M8
                  +-> M6 (F3 needs M5)-+
                  +-> M7 --------------+
```

- M4 requires a frozen `clean_vN` from M2 and split boundaries from M3.
- M5 requires a locked gold set from M4.
- M6 baselines can start after M2; feature group F3 requires M5 outputs.
- M7 requires only M2 outputs and can run in parallel with M4/M5.

## Tiers and cut line

| Tier | Milestones | Rationale |
|---|---|---|
| Core | M0, M1, M2, M3, M4, M5, M6, M8 | Covers data engineering, measurement, modeling and communication |
| Extended | M7 | Adds unsupervised, network and temporal depth |
| Stretch | Hybrid extractor, anomaly, active learning, dashboard | Nice to have |

Cut order under time pressure: Stretch, then M7, then the T2 sensitivity analyses. Modeling (M6) stays in the core because predictive modeling with sound validation is central to data science work.

## Stage gates

| Gate | Condition to proceed |
|---|---|
| M2 to M3 | All quality gates G1-G5 pass; cleaning audit meets 90% threshold |
| M3 to M4 | `clean_v1` frozen; split boundaries decided; guidelines drafted |
| M4 to M5 | Agreement targets met; test ids hash committed |
| M5 to M6 (F3) | Best extraction system selected on dev only |
| M8 release | Reproducibility checklist and ethics checklist complete |

## Definition of done (every milestone)
1. Code in `src/inboxgent` with unit tests; coverage targets met for core modules.
2. Notebooks (if any) run top to bottom and state question, method, result, conclusion.
3. Data-quality gates pass; lineage updated.
4. Results logged in the experiment tracker with run IDs.
5. Findings added to the draft report, including what did not work.
6. `milestone-status.md` updated; milestone tagged in git.
7. Ethics checklist re-checked for any new artifact.

## Pacing guidance
Roughly one milestone per one to two weeks at part-time effort. M4 (annotation) and M2 (cleaning iteration) are the usual schedule risks.
