# Ethics, Privacy and Responsible Use

The dataset consists of real people's workplace email. Public availability does not remove the obligation to handle it carefully.

## 1. Principles
1. Minimize exposure: publish aggregates and labels, not message text.
2. Do no harm: no claims about the conduct of named individuals.
3. Be transparent: document limitations, biases and intended use.
4. Respect the source: follow the dataset's terms and honor removal requests.

## 2. Data handling rules

| Rule | Implementation |
|---|---|
| No raw or cleaned email text in the repository | `.gitignore`, pre-commit blocks, `nbstripout` on notebooks |
| Gold labels stored as ids, offsets, hashes and labels | ADR-006; `surface` text omitted for sensitive strings |
| Figures and examples must not reveal personal details | Redaction (Presidio plus custom regex) and manual review before publication |
| Quoted examples in reports use synthetic or heavily redacted text | Synthetic fixtures for tests and documentation |
| Local data stays local | Raw and interim directories never synced to cloud storage |

## 3. PII policy
- Detect categories: phone numbers, email addresses (outside aggregate network analysis), street addresses, SSN-like patterns, payment-card-like patterns, account numbers.
- Network analysis uses pseudonymous node identifiers in published figures; mapping tables are not committed.
- Any discovered sensitive personal data is recorded by category and count only, not content.

## 4. LLM API usage
- Only content from the public corpus is sent to external APIs; no private mail.
- Redact obvious sensitive patterns before sending where the task does not require them.
- Review the provider's data-use terms and configure for no training on API data where available.
- Log what was sent (hashes and counts), not content.

## 5. Fairness and bias considerations
- No inference of demographic or sensitive attributes (ADR-010).
- Performance slices by custodian, period and message length reveal uneven quality across user groups without profiling individuals.
- Sample selection bias acknowledged: custodians are mostly senior employees of one company in a specific era.
- Language bias: the corpus is largely English business writing; model results should not be assumed for other languages or registers.
- NER bias: pretrained NER systems perform unevenly across name origins; if observed in error analysis it is reported as a limitation without attributing ethnicity to individuals.

## 6. Interpretation and communication guardrails
- Temporal and network findings are descriptive. Alignment with public events does not imply causation or wrongdoing.
- Individual-level conclusions (for example about a particular person's role in events) are out of scope.
- Exploratory results are labeled exploratory.
- The report states that the corpus is historical and unrepresentative of present-day email.

## 7. Intended use and misuse
- **Intended:** methodology research, education, portfolio demonstration.
- **Misuse risks:** surveillance-style profiling of employees; automated judgments about individuals' behavior; re-identification.
- **Mitigation:** the model card states that models are not validated for monitoring individuals or making employment decisions.

## 8. Licensing and attribution
- Cite the corpus and processing sources.
- Code license chosen at M0 (see open questions); documentation licensed permissively.
- Third-party model and library licenses reviewed (spaCy models, sentence-transformers, LLM API terms).

## 9. Takedown and corrections
Contact information in the README. If a person or rights holder requests removal of any derived artifact keyed to their data, the associated labels and figures will be removed in a new release.

## 10. Checklists

### Before first push of any data-derived artifact
- [ ] Contains no email text or personal identifiers
- [ ] Figures reviewed for names and addresses
- [ ] Labels keyed by ids only

### Before final release
- [ ] Datasheet and model card complete
- [ ] Limitations and ethics sections in the findings report
- [ ] PII scan on all committed files
- [ ] License and attribution verified
