# Delivery Workflow: Definition of Ready, Definition of Done and Push Pipeline

How a task moves from "planned" to "merged and trustworthy". Applies to every task in [milestone-stories](milestone-stories.md).

## 1. Definition of Ready (DoR)

A task may be started only when all items are true. If an item fails, the task stays in the backlog and the blocker is recorded in [milestone-status](milestone-status.md).

### Task-level DoR
- [ ] Linked to a user story ID and requirement ID(s).
- [ ] Acceptance criteria are written and testable (a command, a test, a metric threshold or an inspection checklist).
- [ ] All "Depends on" tasks are done, or a stub or fixture is agreed so work can proceed.
- [ ] All "Blocked by gap" items are answered in the [gap register](gap-register.md), or the proposed default has been explicitly accepted.
- [ ] Size is S, M or L. An XL task is split into smaller tasks first.
- [ ] Inputs exist: data version or manifest hash, fixtures, config keys, credentials (via environment, never in the repo).
- [ ] Test approach is known: which unit, property, data-validation or leakage tests will prove it.
- [ ] Privacy and security impact checked: does it touch real email text, PII, secrets or spend?
- [ ] Methodology impact checked: does it change a hypothesis, metric, split or threshold? If yes, an amendment to [problem framing](../01-overview/problem-framing.md) is prepared first.

### Milestone-level DoR
The milestone's **Entry criteria** in [milestone-stories](milestone-stories.md) are met, and the stage gate from the previous milestone in [milestones-foundation](milestones-foundation.md) has passed.

## 2. Definition of Done (DoD)

Done means verified, not just written.

### Task-level DoD (all tasks)
- [ ] Acceptance criteria demonstrably met, with evidence (test output, metric table, audit result).
- [ ] Code lives in `src/inboxgent`; no logic hidden in notebooks.
- [ ] Unit tests added or updated; relevant property, data-validation and leakage tests pass.
- [ ] Lint, formatting and type checks pass; no new security findings.
- [ ] Data-quality gates for the affected stage pass; lineage record updated.
- [ ] No email text, PII, secrets or large files in the diff.
- [ ] Docs updated where behavior, schema, parameters or decisions changed (LLD, decision log, gap register, risks).
- [ ] Commit messages follow the convention below and reference the task ID.
- [ ] Pushed through the pipeline in section 4 with all required checks green.
- [ ] [milestone-status](milestone-status.md) updated if progress or blockers changed.

### Additional DoD by task type

| Task type | Extra conditions |
|---|---|
| Analysis notebook | States question, method, result, conclusion; runs top to bottom on the fixture in CI; outputs stripped; figures cite run IDs; uncertainty intervals shown; negative results recorded |
| Cleaning or parsing | Lineage shows rows and characters affected per step; audit sample reviewed; idempotence and no-growth property tests pass |
| Annotation | Guidelines version recorded; `text_sha256` matches; agreement computed; labels contain ids and offsets only, no text |
| Extraction system | Implements the common interface; evaluated on dev only until test is unlocked; failures counted, not dropped; cost and latency logged |
| Model | Baselines reported alongside; leakage tests green; split scheme stated; calibration and CIs reported; run logged with data manifest hash and git SHA; model card updated |
| Statistical procedure | Reference-value test against a known answer; seeds explicit; primary versus exploratory status declared |
| Documentation | Links resolve; IDs consistent across documents; change recorded in the relevant change log |
| Infrastructure or security | Verification test exists and passes (for example fake secret rejected); documented in [security](../03-tech/security.md) |

### Story-level DoD
A story is done when all its tasks are done and its acceptance criteria in [user-stories](../02-requirements/user-stories.md) are verified.

### Milestone-level DoD
As defined in [milestones-foundation](milestones-foundation.md): all tasks done, exit criteria in [milestone-reference](milestone-reference.md) met, findings added to the draft report including what did not work, ethics checklist re-checked, status updated and the milestone tagged.

## 3. Branch and commit conventions

### Branches
- `main` is always releasable and protected (after M0-10).
- Work branches: `<milestone>/<short-topic>`, for example `m2/quote-stripping`, `m5/llm-backend`, `docs/gap-register`.

### Commit messages (Conventional Commits)
```
<type>(<scope>): <imperative summary>

<optional body: why, not what>

Task: M2-02
```
- **Types:** `feat`, `fix`, `test`, `refactor`, `docs`, `chore`, `ci`, `build`, `perf`, `data` (labels and manifests only).
- **Scopes:** `ingest`, `parse`, `cleaning`, `dedup`, `threading`, `extract`, `evaluate`, `models`, `analysis`, `security`, `tooling`, `planning`, `design`, `requirements`.
- **Granularity:** one logical change per commit. Documentation changes are committed one file per commit so history shows clear incremental contribution.
- Never commit data, secrets or notebook outputs.

### Merging
Use rebase-merge or a merge commit so per-file and per-change commits are preserved. Avoid squash merges for work whose history should remain granular (see gap G-36).

## 4. Push pipeline

```
 edit
  |
  v
 [1 commit-msg + pre-commit]  local, seconds
  |  format, lint, secret scan, security lint, data-path and size blockers,
  |  notebook output strip, conventional-commit check, fast unit tests
  v
 [2 pre-push]                 local, under a few minutes
  |  full unit and property tests on changed modules, type check,
  |  leakage tests, test-id hash check, refuse direct push to main
  v
 push to work branch
  |
  v
 [3 CI on pull request]       remote
  |  install from lock file, lint, types, tests with coverage,
  |  pip-audit, secret scan, bandit/semgrep, fixture pipeline end to end,
  |  notebook execution on fixture, docs link check
  v
 [4 review and merge gate]
  |  all required checks green, PR template checklist complete,
  |  CODEOWNERS review for data/labeled, config, .github
  v
 merge to main
  |
  v
 [5 post-merge]
     main CI re-run, coverage and metrics artifacts archived,
     status doc updated, tag at milestone end, changelog entry
```

### Stage details

| Stage | Where | What runs | Blocks on failure |
|---|---|---|---|
| 1 commit-msg and pre-commit | Local, on `git commit` | ruff format and lint, `detect-secrets`, bandit, data-path blocker, file-size blocker, nbstripout, commit message format, fast unit tests | The commit |
| 2 pre-push | Local, on `git push` | Full tests for changed modules, mypy on selected modules, leakage tests, test-id hash check, guard against pushing to `main` | The push |
| 3 CI | GitHub Actions on every push and PR | Lock-file install, lint, types, full tests with coverage thresholds (80% on core modules), `pip-audit`, secret scan, static security scan, fixture pipeline, notebook run on fixture, link check | The merge (required checks) |
| 4 Review gate | GitHub PR | PR template: no data, no secrets, tests added, docs updated, hypotheses unchanged or amended, task IDs referenced; CODEOWNERS approval where applicable | The merge |
| 5 Post-merge | GitHub | Re-run on `main`; archive evidence artifacts (test report, coverage, lint and security reports, metric tables); milestone tag; changelog | The release |

### Evidence artifacts
Each CI run uploads a small evidence bundle: test results, coverage, security scan reports, data-quality gate reports and (for analysis tasks) the metrics tables with run IDs. The bundle is the proof used when checking a task against its DoD.

### Hook implementation
Hook scripts live in a versioned `.githooks/` directory and are enabled with `make hooks` (sets `core.hooksPath`), delegating to the pre-commit framework configuration. This keeps hooks reviewable and identical for every clone.

### When a stage fails
1. Read the failure; fix the cause, not the check.
2. Do not bypass hooks (`--no-verify`) or disable required checks. If a check is wrong, change the check in its own reviewed commit.
3. If a secret or data file was committed, follow the incident steps in [security](../03-tech/security.md) before anything else.

## 5. Current state versus target

| Aspect | Today | Target |
|---|---|---|
| Hooks | None | Delivered in M0-05 |
| CI | None | Delivered in M0-07 and M0-08 |
| Branch protection | None; documentation is pushed directly to `main`, one file per commit | Enabled in M0-10 (see gaps G-07); all later work through pull requests |
| Evidence artifacts | None | Delivered with M0-07 |

Until M0-10 is done, documentation-only commits go straight to `main`. After M0-10, every change uses a branch and a pull request, including documentation.

## 6. Pipeline-related task mapping

| Task | Delivers |
|---|---|
| M0-05 | Stage 1 hooks (pre-commit and commit-msg) and `.githooks` wiring |
| M0-07 | Stage 3 CI and evidence artifacts |
| M0-08 | Dependency audit and Dependabot |
| M0-09 | PR template, CODEOWNERS |
| M0-10 | Branch protection and required checks (Stage 4) |
| M0-12 | Tests proving the pipeline's security controls work |
| M8-06 | Stage 5 release tag and changelog |
