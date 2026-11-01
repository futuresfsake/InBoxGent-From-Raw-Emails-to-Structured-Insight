# Gap Register: Items Needing a Product Owner Answer

Every open question, provisional assumption, unverified fact and unmade decision in the project, consolidated in one place. All items are owned by the **Product Owner** (the project author) unless stated otherwise.

**How to use:** fill in the *Answer* column and date, then update the referenced document. If an item is not answered by its *Needed by* milestone, the *Proposed default* applies and the item is marked "Defaulted".

**Types:** D = decision, P = provisional parameter (chosen without evidence, needs sign-off or data), F = unverified fact, S = scope/priority.

**Status legend:** Open, Answered, Defaulted.

Last updated: 2026-11-01. Open items: 35.

---

## A. Needed before M0 (foundation and security)

| ID | Type | Question for the Product Owner | Why it matters | Proposed default | Ref | Answer |
|---|---|---|---|---|---|---|
| G-01 | S | What is the target date for having this portfolio ready (e.g., internship application deadline)? | Sets the cut line and pacing | Assume no hard deadline; keep Core tier only if under 8 weeks | new | |
| G-02 | S | How many hours per week can you commit? | The one-to-two-weeks-per-milestone pacing is an assumption | 8 to 10 hours per week | new | |
| G-03 | S | Which type of data science role are you targeting most (ML modeling, NLP, analytics/BI, data engineering)? | Decides which tracks to emphasize in the README and report | Balanced; lead with extraction benchmark and modeling | new | |
| G-04 | D | Should the repository be public from the start or private until release? | Public history is visible to recruiters but exposes drafts and early mistakes; privacy controls must be solid first | Public, after security hooks are in place | new | |
| G-05 | D | Can your LLM provider account create a dedicated API key or workspace with a provider-side spend limit? | Primary defense against runaway spend and key-leak impact | If not, in-code cap plus a low prepaid balance | Q-17 | |
| G-06 | D | GitHub authentication method: SSH key with passphrase or fine-grained token with expiry? | Credential security and convenience | SSH key with passphrase | Q-18 | |
| G-07 | D | Require a pull request and green checks for every change to `main`, or relax to required checks only? | Governance versus speed for a solo repo | Require PRs and green checks | Q-19 | |
| G-08 | D | Code license: MIT, Apache-2.0 or other? Documentation license? | Reuse terms and attribution | MIT for code | Q-12 | |
| G-09 | D | Experiment tracking: MLflow or lightweight CSV/JSON logs? | Overhead versus traceability | MLflow with local store | Q-13 | |
| G-10 | D | What contact address goes in the README and `SECURITY.md` for security reports and takedown requests? | Required by the ethics plan | A dedicated project email or GitHub issues | new | |

## B. Needed by M1 to M3 (data, cleaning, EDA)

| ID | Type | Question for the Product Owner | Why it matters | Proposed default | Ref | Answer |
|---|---|---|---|---|---|---|
| G-11 | D | Main-study sample size: 20k, 30k, 35k or 50k messages? | Runtime, embedding cost, strength of conclusions | 30k canonical messages | Q-01 | |
| G-12 | F | Confirm corpus facts: total message count, number of custodians, date range, attachment handling, version and any removed messages. | The datasheet states expectations from literature; they must be verified by profiling | Verify during M1; correct the datasheet | datasheet | |
| G-13 | D | Dedup method and threshold: MinHash with Jaccard 0.85, or embedding similarity? | Leakage control versus recall | MinHash 0.85, tuned on 100 audited pairs | Q-06 | |
| G-14 | P | Is a 90% pass rate on the 100-email cleaning audit the right acceptance bar? | Gate between M2 and M3 | 90% | spec | |
| G-15 | P | Mass-mail cutoff (50 recipients) and thread time window (30 days): acceptable starting values? | Affects network results, T2 labels and threading accuracy | 50 recipients, 30 days, revisit after EDA | LLD | |
| G-16 | D | How to treat automated and mass-mailed messages: exclude, flag, or model separately? | Affects T1, T2 and network analysis | Flag; exclude from T2; down-weight in network | Q-07 | |
| G-17 | D | Temporal split boundaries: earliest 70% train, next 15% validation, latest 15% test? | Defines test difficulty and per-period sample size | 70/15/15 by date, adjusted after EDA | Q-08 | |
| G-18 | D | Reply window W: 24 hours only, or 24 as primary with 72 as sensitivity? | Defines the T2 label | 24h primary, 72h sensitivity | Q-09 | |

## C. Needed by M4 and M5 (annotation and extraction)

| ID | Type | Question for the Product Owner | Why it matters | Proposed default | Ref | Answer |
|---|---|---|---|---|---|---|
| G-19 | D | Who is the second annotator? If nobody, accept intra-annotator re-labeling after two weeks as a documented limitation? | Credibility of inter-annotator agreement | Intra-annotator re-labeling of 25% | Q-02 | |
| G-20 | D | Which entity fields are in the schema: person, organization, date, amount, action item, and optionally location? | Annotation effort and evaluation scope | First five fields | Q-05 | |
| G-21 | D | Confirm the T1 category taxonomy (business, personal, other) and its written definitions, or propose another. | Defines the label and the labeling guide | Business, personal, other (automated) | new | |
| G-22 | D | Is there a usable external category-labeled subset of the corpus, and are its terms acceptable? | Could reduce T1 labeling effort | Not used; hand-label about 400 | Q-04 | |
| G-23 | P | Gold set size (300 target, 200 floor), T1 label count (about 400) and double-annotated share (25%): acceptable? | Annotation time is the largest schedule risk | 300 / 200 / 400 / 25% | spec | |
| G-24 | P | Agreement targets: kappa 0.70 and span F1 0.80. Acceptable bars? | Decides whether guidelines must be revised | 0.70 and 0.80 | eval method | |
| G-25 | P | Hypothesis thresholds: equivalence margin of 5 F1 points (H1), minimum meaningful effect +0.01 PR-AUC (H4), 90% quality at 25% cost (H2). Sign off before test data is touched? | These are pre-registered; changing them after seeing results undermines the study | As written | problem framing | |
| G-26 | D | LLM budget cap and which two tiers to compare (default `claude-haiku-5-5` and `claude-sonnet-5-5`)? | Feasibility of H1 and H2 | Cap set after a dry-run estimate | Q-03 | |
| G-27 | F | Confirm that the named model identifiers are valid, available to your account, and priced as expected at run time. | Written from general knowledge; pricing and availability change | Check provider documentation in M5 | tech stack | |
| G-28 | D | spaCy model: small only, or also the transformer model? | Baseline strength versus runtime | Both if time allows, reported separately | Q-16 | |
| G-29 | D | Commit LLM response caches? | Reproducibility versus privacy and repo size | No text committed; hashes and metrics only; responses archived privately | Q-11 | |

## D. Needed by M6 to M8 (modeling, extended analysis, release)

| ID | Type | Question for the Product Owner | Why it matters | Proposed default | Ref | Answer |
|---|---|---|---|---|---|---|
| G-30 | S | Include survival analysis of time-to-reply as an extension of T2? | Richer than binary labels but adds scope | Skip (Stretch) | Q-10 | |
| G-31 | D | Which public events and sources form the pre-registered event list for H5, and is a window of +/-4 weeks acceptable? | Must be fixed before change-point runs to avoid post-hoc fitting | Compile from reputable public timelines; commit before M7 | Q-15 | |
| G-32 | S | Which Stretch items, if any, should be built: cascade extractor, anomaly detection, active learning, dashboard? | Scope and time | None until Core is done; then cascade first | tiers | |
| G-33 | D | Build the Streamlit dashboard, and where would it be hosted? | Optional polish; hosting needs a decision | Skip unless M8 finishes early | Q-14 | |
| G-34 | F | Verify every citation (authors, years, venues) before it appears in the final report. | References were written from memory | Check each against its source in M8 | milestone reference | |
| G-35 | S | Is Extended tier (topics, network, change points) mandatory for your goals, or may it be cut if time is short? | Defines cut order | Cut Stretch first, then Extended | milestones foundation | |

---

## Work items that are not gaps

These are planned tasks with no open question, listed so they are not mistaken for decisions: write `.gitignore`, `LICENSE`, `SECURITY.md`, `CODEOWNERS`, PR template, pre-commit config, CI workflows, annotation guidelines, event list file, threat-model verification tests, synthetic fixture dataset.

## Summary by milestone

| Needed by | Open items |
|---|---|
| M0 | G-01 to G-10 (10) |
| M1 to M3 | G-11 to G-18 (8) |
| M4 to M5 | G-19 to G-29 (11) |
| M6 to M8 | G-30 to G-35 (6) |

## Change log

| Date | Change |
|---|---|
| 2026-11-01 | Register created from open questions Q-01 to Q-19, provisional parameters, unverified facts and newly identified decisions. |
