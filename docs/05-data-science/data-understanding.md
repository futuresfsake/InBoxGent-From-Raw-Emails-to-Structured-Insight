# Dataset Datasheet and Data Understanding

Structured after "Datasheets for Datasets" (Gebru et al.). Items marked **[verify in M1]** are expectations from the literature that must be confirmed by profiling before being stated as fact in the findings.

## 1. Motivation
- **Purpose:** a public, realistic corpus of workplace email for studying cleaning, extraction, classification and network analysis.
- **Origin:** email from Enron Corporation employees, made public during the federal investigation of the company and later processed for research use at Carnegie Mellon University. It is widely used in academic work (see Klimt and Yang, 2004).
- **Why this dataset:** public, large, realistic noise, a known external event timeline, and a long research history for comparison.

## 2. Composition
- **Unit of observation:** one email message.
- **Scale [verify in M1]:** on the order of half a million messages from roughly 150 custodians, mostly senior management.
- **Structure:** one directory tree per custodian containing folders (inbox, sent, deleted items, and others) with one message per file in RFC 822 style.
- **Time span [verify in M1]:** concentrated between 1999 and 2002, with the heaviest volume in 2000-2001; parse errors may produce spurious dates such as 1970 or future dates.
- **Content:** business correspondence, internal announcements, trading and legal topics, personal messages, and automated mail.
- **Attachments:** removed in the research release [verify in M1].
- **Sensitive content:** real names, addresses, phone numbers and potentially other personal details. Treated under the [ethics and privacy plan](ethics-and-privacy.md).

## 3. Known data quality issues (expected)

| Issue | Expected impact | Planned handling |
|---|---|---|
| Duplicate messages across folders (e.g., sent, all documents, discussion threads) | Inflated counts; train/test leakage | Exact dedup on full corpus; near-dup clustering; cluster-grouped splits |
| Invalid or default dates | Corrupted time series | Range validation; null and exclude from temporal analysis |
| Quoted history and forwards | Repeated text inflates frequencies; biases topics and classifiers | Cleaning step with lineage; ablation H3 |
| Signatures and legal boilerplate | Spurious entity matches | Boilerplate learning and removal |
| Mass-mailings and distribution lists | Distorts network metrics | Edge weighting; exclusion sensitivity |
| Automated or system-generated mail | Different statistical profile | Flagging; stratified reporting |
| Header anomalies and inconsistent address forms | Entity resolution errors | Address normalization; failure counts |
| Custodian-only coverage | Missing counterpart mailboxes | Restrict T2; document in limitations |

## 4. Collection and provenance
- Collected by investigators; later cleaned and redistributed for research. Some messages were removed on request for privacy reasons and some integrity problems were corrected in later releases [verify in M1].
- The dataset is not a random sample of all Enron communications and not a representative sample of workplace email in general.

## 5. Preprocessing in this project
- Parsing, cleaning, deduplication and threading as defined in the [LLD](../04-design/lld.md).
- Every transformation recorded in lineage logs; raw text is always retained internally.

## 6. Sampling plan
- **Sampling frame:** deduplicated messages with a valid date and non-empty body.
- **Design:** stratified by custodian and year, seeded, with inclusion probabilities stored.
- **Size:** 20,000 to 50,000 messages for the main study (final size set in M1; see open questions).
- **Gold set:** about 300 emails drawn from the main sample by stratified random selection at natural prevalence. A small separate "hard case" set (long threads, forwarded chains, tabular content) is annotated and reported separately so as not to distort prevalence.
- **Bias note:** stratification gives balance across custodians and years but does not equal population representativeness; weighted estimates use inclusion probabilities where relevant.

## 7. Profiling plan (M1 and M3)
- Missingness by column, custodian and year
- Date validity and distribution
- Message length distributions (raw and cleaned)
- Recipient count distribution and mass-mail share
- Duplicate rates exact and near
- Top boilerplate n-grams
- Language and encoding checks
- Folder and custodian composition

Outputs: profiling report committed as figures and summary tables without email text.

## 8. Recommended and discouraged uses
- **Recommended:** methodology demonstration for cleaning, extraction, classification, network and temporal analysis.
- **Discouraged:** claims about the culpability of any individual; modern-email generalization without validation; inferring personal attributes.

## 9. Distribution and licensing
- The raw corpus is downloaded by the user from its public source; it is not redistributed in this repository.
- This repository contains code, documentation, aggregate results and annotation labels keyed by message id.

## 10. Maintenance
- Data version identified by the checksum manifest. If the upstream corpus changes, the manifest changes and results must be regenerated.
- Known issues and corrections recorded in the changelog.

## 11. Open data questions
Tracked in [open-questions](../06-planning/open-questions.md): final sample size, handling of automated mail, whether to use externally available category labels.
