# Security and Access Management

InBoxGent is a local batch pipeline with no end users, so there is no user authentication to build. Security here means protecting credentials, protecting data about real people, securing the software supply chain, and controlling who can change the repository. This document is delivered in milestone M0.

## 1. Assets

| Asset | Why it matters |
|---|---|
| Anthropic API key | Leakage allows spend by others and account abuse |
| GitHub credentials (SSH key or token) | Leakage allows unauthorized changes to the repository |
| Raw and cleaned email text | Real people's correspondence; privacy obligations |
| Gold labels and test-id lock | Integrity of the evaluation |
| LLM response cache | May contain email-derived text |
| Experiment logs (`mlruns`) | May contain data-derived artifacts |
| Repository history | Anything committed is effectively permanent |

## 2. Threat model

| ID | Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| T-01 | API key committed to git | Medium | High | `.env` git-ignored, `detect-secrets` pre-commit hook, CI secret scan, key rotation procedure |
| T-02 | API key exposed in logs, notebooks or error traces | Medium | High | Never log secrets; redact in logger; `nbstripout`; config object masks secret fields in `repr` |
| T-03 | Runaway LLM spend (bug, loop, leaked key) | Medium | Medium | Dedicated key with provider-side spend limit; in-code budget cap; dry-run estimates |
| T-04 | Email text or PII committed to the repository | Medium | High | `.gitignore` for data directories; pre-commit path and size blockers; PII scan; manual review before release |
| T-05 | Malicious or vulnerable dependency | Low | High | Locked dependencies; `pip-audit` in CI; Dependabot alerts; review before upgrades |
| T-06 | Compromised GitHub account | Low | High | 2FA; SSH key with passphrase or fine-grained token with expiry; no tokens in repo |
| T-07 | Unreviewed or broken changes reaching `main` | Medium | Medium | Branch protection, required CI, PR template |
| T-08 | Malicious content in downloaded data or models | Low | Medium | Verify checksums; treat the corpus as untrusted text; never execute downloaded files; pin model sources |
| T-09 | Prompt injection through email content sent to an LLM | Medium | Low | LLM output only parsed against a schema; no tool use or code execution on model output; outputs never trusted for control flow |
| T-10 | Test-set tampering or accidental modification | Low | High | Test-id hash committed; CI test verifies the hash; CODEOWNERS on `data/labeled/` |
| T-11 | Secrets or data leaking via CI logs or artifacts | Low | Medium | CI uses only the fixture dataset; no real API key in CI; masked secrets if ever added |

## 3. Credential and access management

### API key
- Create a dedicated key for this project with a spend limit set at the provider.
- Load only from the `ANTHROPIC_API_KEY` environment variable; a local `.env` file (git-ignored) is allowed for development.
- `.env.example` is committed with placeholder names only.
- The config loader treats the key as a secret type (masked output).
- Rotation: revoke and replace on any suspected exposure; document the steps in `SECURITY.md`.
- CI does not receive the key; LLM code is tested with mocks.

### GitHub
- Enable two-factor authentication.
- Use SSH keys protected by a passphrase, or a fine-grained personal access token limited to this repository with an expiry date.
- Never embed credentials in remote URLs stored in the repo configuration.

### Repository governance
- Branch protection on `main`: require pull requests, require passing CI checks, disallow force pushes and deletions.
- `CODEOWNERS` assigns ownership for `data/labeled/`, `config/` and `.github/`.
- PR template includes a checklist: no data, no secrets, tests added, docs updated, hypotheses unchanged or amended.
- Signed commits are optional; recommended if configured.

## 4. Data protection controls
- `.gitignore` covers `data/raw`, `data/interim`, `data/features`, `data/outputs`, `mlruns`, `.env`, caches.
- Pre-commit blockers: any file under ignored data paths, files above a size threshold, files with email-like header patterns.
- `nbstripout` strips notebook outputs.
- PII detection (Presidio plus regex) runs before any publication step.
- The LLM cache and outputs stay local; only hashes and aggregate metrics are shareable.

## 5. Supply chain
- Lock file committed; installation in CI is from the lock file only.
- `pip-audit` runs in CI and fails on known high-severity vulnerabilities.
- Dependabot configured for Python dependencies and GitHub Actions.
- GitHub Actions pinned to commit SHAs or trusted major versions; workflow permissions set to least privilege (`contents: read`).
- spaCy and embedding models downloaded from official sources; model names and versions recorded.

## 6. Secure development practices
- Input handling: email content is treated as untrusted; no `eval`, no shell execution on content; regex patterns reviewed for catastrophic backtracking and run with timeouts on large inputs.
- Error handling: do not echo raw email text or secrets into error messages or logs.
- Least privilege: pipeline stages read only the paths they need; output directories are separate from inputs.
- Static analysis: `ruff` with security-relevant rules (including flake8-bandit equivalents) and `bandit` in CI.

## 7. Incident response (lightweight)
1. **Key exposure:** revoke at the provider, create a new key, scrub from history if committed (rewrite history only with care and after revocation), review provider usage logs.
2. **Data exposure:** remove from the repo, assess whether history rewrite is needed, record the incident in `SECURITY.md`'s changelog, notify the dataset source if required.
3. **Dependency vulnerability:** upgrade or pin; rerun tests; document.

## 8. Verification
| Control | How verified |
|---|---|
| Secret scanning | Test commit containing a fake key is rejected by the hook; CI scan job present |
| Data blockers | Attempt to add a file under `data/raw` is rejected |
| Config masking | Unit test asserts the key does not appear in `repr` or log output |
| Budget cap | Unit test with mocked client stops at the cap |
| Branch protection | Direct push to `main` blocked once enabled; PR required |
| Dependency audit | CI job runs `pip-audit` on every push |
| Test lock | CI test recomputes the test-id hash and compares |

## 9. Deliverables in M0
`SECURITY.md`, `.env.example`, `.gitignore`, pre-commit config, CI workflows (lint, tests, audit, secret scan), Dependabot config, `CODEOWNERS`, PR template, `LICENSE`, this threat model, and the tests listed above.
