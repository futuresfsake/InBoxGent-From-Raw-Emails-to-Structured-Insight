# Testing Strategy

Data science projects fail quietly, so testing covers code correctness, data quality and model validity.

## Levels

### 1. Unit tests (pytest, `tests/`)
Target the pure functions in `src/`.
- **Parsing:** malformed headers, missing Date, multiple recipients, odd encodings.
- **Cleaning:** each step on small hand-written fixtures (nested quotes, forwarded chains, signatures with and without delimiters).
- **Dedupe:** identical, near-identical and distinct messages.
- **Evaluator:** known prediction/gold pairs with hand-computed precision, recall and F1.
- **Extractor interface:** each backend returns the expected types on a tiny sample; LLM backend tested with a mocked client.

### 2. Data validation checks
Run after each pipeline stage; fail loudly.
- Schema and dtype match the LLD.
- `message_id` unique after dedupe flagging.
- Date range plausible (no future dates, no 1970 defaults).
- Null rates under agreed thresholds.
- Body length distribution sanity check before and after cleaning.

### 3. Pipeline integration test
A tiny fixture dataset (about 20 emails, committed) runs end to end in under a minute and produces expected row counts.

### 4. Manual validation
- Spot check 50 cleaned emails against the 90% acceptance criterion.
- Double-annotation of 20% of the gold set to estimate label consistency.

### 5. Model validation
- Fixed random seeds, stratified splits, no test-set tuning.
- Majority-class and simple baselines always reported next to the main model.
- Check for leakage: duplicates must not span train and test; features must not contain the label source (e.g. folder name if folder defined the label).
- Cross-validation variance reported, not just the mean.

## Coverage goals
- At least 80% line coverage on `cleaning.py`, `parse.py`, `evaluate.py`.
- No coverage target for notebooks; they must run top to bottom without error.

## Tooling
- pytest, pytest-cov
- ruff for linting
- pre-commit hooks for lint and a fast test subset
- Optional GitHub Actions workflow to run lint and tests on push

## Test data policy
Only public Enron samples or synthetic emails in the repo. No personal email, ever.
