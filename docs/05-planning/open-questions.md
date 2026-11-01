# Open Questions

Track decisions that are not yet made. Move resolved items to the bottom with the decision and date.

## Open

| ID | Question | Why it matters | Needed by |
|---|---|---|---|
| Q-01 | What sample size should we use: 20k, 50k, or the full corpus? | Affects runtime and the strength of EDA conclusions | M1 |
| Q-02 | Which fields are in scope for extraction: person, org, date, amount, action item, or a subset? | Drives annotation effort and evaluation design | M4 |
| Q-03 | What is the API budget for LLM extraction, and which model tier? | Determines the size of the LLM evaluation | M5 |
| Q-04 | Should a local model (Ollama) be added as a fourth backend? | Adds a free comparison point but more work | M5 |
| Q-05 | How are `business` vs `personal` labels produced: manual, folder heuristic, or both? | Risk of leakage and label noise | M6 |
| Q-06 | Should near-duplicate detection use MinHash or embedding similarity? | Trade-off between speed and accuracy | M2 |
| Q-07 | Do we build the Streamlit dashboard, and where is it hosted? | Optional but impressive; hosting needs a decision | M8 |
| Q-08 | Do we commit LLM response caches to the repo? | Reproducibility versus repo size | M5 |
| Q-09 | What license should the repo use? | Affects reuse by others | M0 |
| Q-10 | Do we set up GitHub Actions CI now or later? | Cheap quality signal for reviewers | M0 |

## Resolved

| ID | Question | Decision | Date |
|---|---|---|---|
| Q-00 | What is the project name? | InBoxGent: From Raw Emails to Structured Insight | 2026-11-01 |
