# Contributing

Read [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) and [docs/architecture/OWNERSHIP.md](docs/architecture/OWNERSHIP.md) first. Read [RECOVERY.md](RECOVERY.md) if you are resuming work.

## Workflow

1. `git fetch origin && git checkout -b <your-branch> origin/main` (branch names are in OWNERSHIP.md).
2. Edit only the files your area owns. Shared files go through the coordinator.
3. Code against the frozen contracts in `docs/architecture/API_CONTRACT.md`. Do not change a signature, response key or constant. If you think a contract is wrong, raise it with the coordinator.
4. Write tests with your code. Services must be testable without network access: mock Groq, use dict fixtures for retrieval, use in-memory SQLite (`sqlite://`) for DB tests.
5. Run `pytest -q`. `tests/test_foundation_contracts.py` must keep passing.
6. Update your section of `TASK_TRACKER.md` and append an entry to `IMPLEMENTATION_LOG.md`.
7. `git fetch origin && git rebase origin/main`, push your branch, open a PR to `main`. Do not merge it yourself.

## PR checklist

- [ ] Only files owned by my area changed (or the PR explains why not)
- [ ] `pytest -q` passes
- [ ] No secrets, `.env`, `*.db` or caches committed
- [ ] Tracker status is honest: a task is `VERIFIED` only if you ran it and saw it work
- [ ] Anything not tested is listed in the PR description

## Rules

- No commits directly to `main`. No force-push. No self-merge.
- Commit messages: `feat:`, `fix:`, `chore:`, `docs:` or `test:` prefix, imperative mood.
- Never fabricate results: services raise or return an explicit non-success status.
- Never hard-code a Groq model ID. A live Groq integration counts as verified only after you have listed the models available to your key and made a successful call with the configured `GROQ_MODEL`.
- Synthetic data only. No real customer, employee or company data.
