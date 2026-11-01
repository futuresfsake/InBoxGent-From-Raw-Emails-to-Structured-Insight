# Milestones Foundation

This document defines how milestones are structured so the rest of the planning docs stay consistent.

## Principles
- Each milestone produces something demonstrable, not just code.
- Milestones are sequenced so the project is presentable after M3 even if time runs out.
- Each milestone has a definition of done, and every item traces back to a requirement or user story.

## Milestones

| ID | Name | Outcome | Requirements | Stories |
|---|---|---|---|---|
| M0 | Foundation | Repo structure, environment, docs, config, CI basics | NFR-01, NFR-03 | |
| M1 | Ingest & Parse | Reproducible sample with structured headers | FR-01, FR-02 | US-01, US-02 |
| M2 | Cleaning | Clean bodies, dedupe, cleaning log | FR-03 to FR-06 | US-03, US-04, US-05 |
| M3 | EDA | First insight report with charts | FR-12 | US-11 |
| M4 | Gold Set | About 200 hand-labeled emails | FR-09 | US-08 |
| M5 | Extraction & Evaluation | Three backends compared on the gold set | FR-07, FR-08, FR-10, FR-11 | US-06, US-07, US-09, US-10 |
| M6 | Classification | Baseline and improved classifier with proper evaluation | FR-13 | US-12 |
| M7 | Topics | Topic model and cluster visualization | FR-14 | US-13 |
| M8 | Polish & Publish | Findings write-up, README summary, optional dashboard | FR-15, NFR-07 | US-14, US-15, US-16 |

## Definition of done (all milestones)
1. Code in `src/`, notebook (if any) runs top to bottom.
2. Unit tests for new core functions pass.
3. Outputs reproducible from the documented run order.
4. Milestone status and findings updated in `milestone-status.md`.
5. Committed with a clear message.

## Cut line
If time is short, ship M0-M5 and M8. M6 and M7 are valuable upgrades but not required for a coherent story.

## Suggested pacing
Roughly one milestone per week at part-time effort; M4 (labeling) is manual and may take longer than its code complexity suggests.
