# Risks

Likelihood (L) and Impact (I): Low, Medium, High.

| ID | Risk | L | I | Mitigation | Owner |
|---|---|---|---|---|---|
| R-01 | Scope creep: project grows beyond what one person can finish | High | High | Fixed cut line (M0-M5 + M8); stretch items clearly marked | Author |
| R-02 | Cleaning heuristics fail on diverse email formats | High | Medium | Log every step, spot check, iterate on failure samples, accept imperfect recall and document it | Author |
| R-03 | Labeling the gold set takes much longer than planned | Medium | High | Shrink to 100 emails minimum; write guidelines first; label a few fields only if needed | Author |
| R-04 | Inconsistent annotations make metrics unreliable | Medium | Medium | Written guidelines; re-label a 20% subset and measure agreement | Author |
| R-05 | LLM API cost exceeds budget | Medium | Medium | Run LLM only on gold set and a capped sample; cache all responses; optional local model fallback | Author |
| R-06 | Data leakage inflates classifier results | Medium | High | Dedupe before splitting; audit features; report baselines | Author |
| R-07 | Enron corpus is dated or unrepresentative of modern email | High | Low | State limitation in write-up; frame findings as method demonstration | Author |
| R-08 | Accidental commit of large raw data or secrets | Medium | High | `.gitignore` from first commit; keys via env vars; pre-commit secret scan | Author |
| R-09 | Dependency or version drift breaks reproducibility | Low | Medium | Pin versions; record Python version; test fresh-clone install | Author |
| R-10 | Time runs out before polish, leaving a weak presentation | Medium | High | Reserve M8; keep README findings updated as milestones finish | Author |
| R-11 | LLM outputs are non-deterministic, hurting reproducibility | Medium | Low | Temperature 0, cached responses committed or documented | Author |
| R-12 | Class labels for classification are noisy or ill-defined | Medium | Medium | Clear label definitions; small manual verification set | Author |

## Review cadence
Revisit this list at the end of each milestone and update likelihood, impact and status.
