# Security Policy

## Reporting a vulnerability or a takedown request
Open a GitHub issue on this repository titled "Security" without including any secret or personal data, or use GitHub's private vulnerability reporting for this repository. Requests to remove a person's data from published artifacts are handled the same way. A dedicated project email may be added here later.

## Scope
This is a local batch data science pipeline with no users or network service. The relevant risks are leaked credentials, committed email text or PII, vulnerable dependencies and unreviewed changes. The threat model and controls are in [`docs/03-tech/security.md`](docs/03-tech/security.md).

## Handling secrets
- The Anthropic API key is read only from the `ANTHROPIC_API_KEY` environment variable or a git-ignored `.env`.
- Use a dedicated key with a provider-side spend limit.
- If a key may have been exposed: revoke it at the provider first, create a new one, review usage logs, then scrub history only after revocation.

## Handling data
No raw or cleaned email text is committed. Only `data/labeled/` (ids, offsets and labels) is tracked.

## Changelog
| Date | Incident or change |
|---|---|
| 2026-11-08 | Policy created. |
