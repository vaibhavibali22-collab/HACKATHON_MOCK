# Recovery

Read this first when resuming after a break, a crashed session or a context loss.

## Last verified state (2026-10-10)

- Branch `chore/project-foundation`, based on `main` at `c8506d8` ("Initial commit"). The tip of the branch is the latest foundation commit (`git log -1`).
- Verified: clean-venv `pip install -r requirements.txt`; `pytest -q` -> 11 passed.
- Not verified: Groq key/model, Python 3.11, any API/UI behaviour (not implemented yet).
- No feature code exists. `app/main.py`, `app/db/*`, `app/api/*`, `frontend/streamlit_app.py` are placeholders; the three service modules raise `NotImplementedError`.

## Next safe task

1. Vaibhavi reviews and merges the foundation PR (`chore/project-foundation` -> `main`).
2. Fill in the owner names in `docs/architecture/OWNERSHIP.md`.
3. Only then start the four feature prompts, each on its own branch from the updated `main`.

Do not start feature work on top of an unmerged foundation branch.

## How to resume

```bash
git fetch origin
git status && git branch --show-current
git log --oneline -5
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
pytest -q
```

Then read `TASK_TRACKER.md` for your area, and the tail of `IMPLEMENTATION_LOG.md`.

## Common recoveries

| Problem | Fix |
|---|---|
| Local DB is corrupt or out of date | stop the backend, delete `tickets.db`, run `python -m app.db.seed` |
| `pytest` fails in `test_foundation_contracts.py` | a frozen contract was changed; revert it or follow the interface-change process in `OWNERSHIP.md` |
| Merge conflict in `IMPLEMENTATION_LOG.md` | keep both entries, newest at the bottom |
| Merge conflict in a shared file | do not resolve it alone; ask the coordinator |
| `.env` missing | `cp .env.example .env` and fill in the values; never commit it |
| Groq calls fail with "model not found/decommissioned" | list models available to your key (command in `.env.example`) and update `GROQ_MODEL` in `.env` |
| Accidentally committed a secret | rotate the key immediately, then tell the coordinator before touching history |
