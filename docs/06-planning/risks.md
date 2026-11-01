# Risk Register

Likelihood (L) and Impact (I): Low, Medium, High. Reviewed at the end of every milestone.

## Methodological risks

| ID | Risk | L | I | Mitigation | Trigger / early signal |
|---|---|---|---|---|---|
| R-01 | Train/test leakage via duplicates or shared threads inflates results | High | High | Dedup before sampling; cluster and thread grouping; automated leakage tests | Test metrics much higher than temporal-split metrics |
| R-02 | Dev/test contamination through prompt or rule tuning | Medium | High | Test locked by hash; few-shot examples from dev only; test evaluated once | Commits touching test labels after lock |
| R-03 | Forking paths and multiple comparisons produce false positives | Medium | High | Pre-registered hypotheses; Holm correction; exploratory label | Many unplanned comparisons in notebooks |
| R-04 | Label noise or low inter-annotator agreement | Medium | High | Guidelines, pilot, double annotation, adjudication, kappa gates | Kappa below 0.70 |
| R-05 | Gold set too small for conclusive comparisons | Medium | Medium | Report CIs; call small differences inconclusive; extend annotation if budget allows | Bootstrap CIs overlapping heavily |
| R-06 | Reply labels are noisy (responder outside corpus, thread errors, right-censoring) | High | Medium | Restrict to observable replies; censoring exclusion; sensitivity on W and thread confidence | Low reply rate in unexpected custodians |
| R-07 | Temporal distribution shift around the 2001 crisis degrades models | High | Medium | Report as finding; slice by period; rolling-origin validation | Large gap between validation and test periods |
| R-08 | Thread reconstruction errors propagate to splits and labels | Medium | Medium | Confidence scores; audit; sensitivity analysis | Audit accuracy under 85% |
| R-09 | Cleaning heuristics over-remove or under-remove content | High | Medium | Lineage logs; audit; ablation; version control for cleaning | Audit failures; sudden drop in body length |
| R-10 | Cleaning changes after annotation invalidate gold labels | Medium | High | Freeze `clean_v1` before M4; hash check in tests | Hash mismatch |
| R-11 | Selection bias from stratified sampling and single-company, single-era data | High | Low | State limitations; weighted estimates where relevant; avoid generalization claims | Reviewer questions on representativeness |
| R-12 | Change-point or network findings become post-hoc storytelling | Medium | Medium | Pre-registered event list; permutation baseline; exploratory label | Narrative drafted before tests run |

## Technical and operational risks

| ID | Risk | L | I | Mitigation | Trigger |
|---|---|---|---|---|---|
| R-13 | LLM API cost overrun | Medium | Medium | Budget cap, dry-run estimates, caching, restrict LLM to gold plus capped sample | Spend near cap |
| R-14 | LLM model deprecation or behavior drift breaks reproducibility | Medium | Medium | Pin model ids; archive raw responses; version prompts | Provider deprecation notice |
| R-15 | Non-determinism in LLM outputs | Medium | Low | Temperature 0; cache is the source of truth | Different outputs on rerun |
| R-16 | Dependency drift breaks installs | Low | Medium | Lock file; CI on fresh install | CI failures after update |
| R-17 | Performance limits on a laptop (near-dup, embeddings) | Medium | Medium | Chunking; LSH; smaller sample; caching embeddings | Stage runtime above budget |
| R-18 | Hardware or time failure loses progress | Low | Medium | Frequent commits; stage artifacts reproducible from manifest | |

## Ethical and privacy risks

| ID | Risk | L | I | Mitigation | Trigger |
|---|---|---|---|---|---|
| R-19 | Accidental commit of email text, PII or secrets | Medium | High | `.gitignore`, pre-commit blockers, secret scan, nbstripout, manual review before release | Hook failures; large files in diff |
| R-20 | Findings misread as claims about individuals' wrongdoing | Low | High | Descriptive framing; pseudonymous nodes; explicit guardrails in report | Named individuals in figures |
| R-21 | Sensitive-attribute inference creeping into analysis | Low | Medium | ADR-010; code review for such features | Features derived from names |

## Project risks

| ID | Risk | L | I | Mitigation | Trigger |
|---|---|---|---|---|---|
| R-22 | Scope creep given the expanded plan | High | High | Tiers; cut order Stretch then Extended; milestone gates | Milestone slipping by more than 50% |
| R-23 | Annotation effort exceeds time | High | High | Floor of 200 emails; hard-case set optional; reduce fields only as last resort | M4 behind schedule |
| R-24 | Time runs out before synthesis | Medium | High | Findings drafted incrementally per milestone; M8 reserved | Draft report empty at M5 |
| R-25 | No second annotator available | Medium | Medium | Intra-annotator re-labeling after two weeks; state limitation | Decision at M4 start |

## Security risks (see [security](../03-tech/security.md) for the full threat model)

| ID | Risk | L | I | Mitigation | Trigger |
|---|---|---|---|---|---|
| R-26 | API key leaked via commit, log or notebook | Medium | High | Env-only loading, `.env` ignored, detect-secrets, masked config, rotation procedure | Secret-scan alert; unexpected provider usage |
| R-27 | Vulnerable or malicious dependency | Low | High | Lock file, `pip-audit`, Dependabot, review before upgrades | Audit failure |
| R-28 | Unreviewed change merged to `main` or GitHub account compromise | Low | High | Branch protection, required checks, 2FA, least-privilege tokens | Unexpected commits or token alerts |
| R-29 | Prompt injection in email content influences pipeline behavior | Medium | Low | Schema-validated outputs only; no execution or tool use on model output | Unexpected output formats |

## Review log

| Date | Change |
|---|---|
| 2026-11-01 | Register expanded from 12 to 25 risks to cover methodological, ethical and operational categories. |
| 2026-11-01 | Added security risks R-26 to R-29 following the M0 security scope. |
