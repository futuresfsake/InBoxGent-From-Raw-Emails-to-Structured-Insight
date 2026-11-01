# Project Overview

## Name
InBoxGent: From Raw Emails to Structured Insight

## Problem
Email is one of the largest sources of unstructured business data, but it is full of noise: headers, signatures, quoted replies, forwarded chains, encoding artifacts and duplicates. Before any analysis can happen, it has to be cleaned and structured.

## Central question
Can we reliably turn messy, unstructured email into structured data, and what does that data reveal about communication patterns?

## Goals
1. Build a reproducible cleaning pipeline for raw email.
2. Extract structured fields (people, dates, amounts, organizations, action items).
3. Compare extraction approaches (rules, classic NLP, LLM) with measured accuracy, cost and latency.
4. Analyze the structured output (EDA, classification, topic discovery).
5. Present findings clearly enough to serve as a data science portfolio piece.

## Non-goals
- Not a production email client or inbox manager.
- No processing of any personal or private mailbox data in the public repo.
- No real-time or streaming ingestion.

## Dataset
Enron email corpus (public), sampled to roughly 20,000-50,000 messages.

## Deliverables
- Cleaning and extraction code in `src/`
- Analysis notebooks in `notebooks/`
- A labeled evaluation set (about 200 emails)
- A findings report with figures
- Optional Streamlit dashboard

## Success criteria
- Cleaning pipeline logs what each step removes and is rerunnable end to end.
- Extraction approaches compared with precision, recall and F1 per field on the labeled set.
- At least one classification model beats a trivial baseline on held-out data.
- A README findings summary a reviewer can read in under five minutes.

## Audience
Data science internship reviewers and hiring managers.
