# Open Questions

Decisions not yet made. Each has an owner, a deadline milestone and a default that will apply if no decision is made.

## Open

| ID | Question | Why it matters | Default if undecided | Needed by |
|---|---|---|---|---|
| Q-01 | Final sample size: 20k, 35k or 50k messages? | Runtime, strength of EDA, embedding costs | 30k canonical messages | M1 |
| Q-02 | Who is the second annotator, or do we use intra-annotator re-labeling? | Inter-annotator agreement credibility | Re-label 25% after two weeks; state limitation | M4 |
| Q-03 | LLM budget cap and which two model tiers to compare? | Defines feasibility of H1 and H2 | `claude-haiku-5-5` vs `claude-sonnet-5-5`, cap set after dry-run estimate | M5 |
| Q-04 | Is there a usable external category-labeled subset of the corpus, and what are its terms? | Could reduce T1 labeling effort | Not used; hand-label about 400 | M4 |
| Q-05 | Which entity fields stay in the primary schema: person, organization, date, amount, action_item, and optionally location? | Annotation cost and evaluation scope | The first five | M4 |
| Q-06 | Dedup threshold and near-dup method (MinHash vs embeddings)? | Leakage control and recall | MinHash Jaccard 0.85, tuned on audit pairs | M2 |
| Q-07 | How to treat automated and mass-mailed messages: exclude, flag or model separately? | Affects T1, T2 and network results | Flag; exclude from T2 and weight in network | M3 |
| Q-08 | Temporal split boundaries? | Determines test difficulty and sample size per period | Train earliest 70% by date, validation next 15%, test latest 15%; adjust after EDA | M3 |
| Q-09 | Reply window W: 24h only, or also 72h? | T2 label definition | 24h primary, 72h sensitivity | M3 |
| Q-10 | Include survival analysis of time-to-reply? | Richer than binary T2 | Stretch; skip | M6 |
| Q-11 | Commit LLM response caches? | Reproducibility versus privacy and repo size | Do not commit text; store hashes and metrics; archive responses privately | M5 |
| Q-12 | Code license (MIT, Apache-2.0) and documentation license? | Reuse and attribution | MIT for code | M0 |
| Q-13 | Experiment tracking: MLflow or lightweight CSV logs? | Overhead versus traceability | MLflow local | M0 |
| Q-14 | Dashboard hosting and whether to build it? | Optional polish | Skip unless M8 finishes early | M8 |
| Q-15 | Event list for H5: which public dates and sources? | Needed before change-point runs to avoid post-hoc fitting | Compile from reputable public timelines; commit before M7 | M7 |
| Q-16 | spaCy model: small or transformer-based? | Baseline strength versus runtime | Both if time allows; report separately | M5 |

## Resolved

| ID | Question | Decision | Date |
|---|---|---|---|
| Q-00 | Project name | InBoxGent: From Raw Emails to Structured Insight | 2026-11-01 |
| Q-R1 | Is predictive modeling core or optional? | Core (ADR-012) | 2026-11-01 |
| Q-R2 | Commit email text in the gold set? | No; labels and ids only (ADR-006) | 2026-11-01 |
| Q-R3 | Random or temporal splits for ML evaluation? | Temporal plus grouped as primary; random grouped as reference (ADR-008) | 2026-11-01 |
