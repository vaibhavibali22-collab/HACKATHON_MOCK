# Ownership and Branch Strategy

Integration coordinator and repository owner: **Vaibhavi**. She reviews and merges every PR into `main`.

The four feature areas are assigned to people or AI coding sessions by the coordinator. Owner names below are placeholders to fill in.

## Areas and file ownership

| Area | Owner | Branch | Files (only this area edits these) |
|---|---|---|---|
| 1. Data layer | TBD | `feat/data-layer` | `app/db/database.py`, `app/db/models.py`, `app/db/seed.py`, `data/synthetic_tickets.json`, `tests/test_db_*.py`, `tests/test_seed*.py` |
| 2. Retrieval | TBD | `feat/retrieval` | `app/services/retrieval.py`, `tests/test_retrieval*.py` |
| 3. LLM service | TBD | `feat/llm-service` | `app/services/llm_service.py`, `tests/test_llm*.py` |
| 4. API, orchestration and frontend | TBD | `feat/api-orchestration-frontend` | `app/main.py`, `app/api/routes.py`, `app/api/schemas.py`, `app/services/resolution_service.py`, `frontend/streamlit_app.py`, `tests/test_api*.py`, `tests/test_resolution*.py` |

### Shared files (coordinator-controlled)

`app/config.py`, `requirements.txt`, `.env.example`, `.gitignore`, `README.md`, `CONTRIBUTING.md`, `PROJECT_CONTEXT.md`, `docs/architecture/*`, `tests/test_foundation_contracts.py`, `tests/__init__.py`, all `__init__.py` files.

- Do not edit shared files in a feature PR. If you need a new dependency, constant or env var, open an issue or message the coordinator; she adds it in a small `chore/` PR first.
- Exception: a feature PR may add dependencies to `requirements.txt` if it says so in the PR description and touches no other shared file. The coordinator decides at review.

### Continuity files

- `TASK_TRACKER.md`: each area edits only its own section.
- `IMPLEMENTATION_LOG.md`: append-only, newest entry at the bottom. On a merge conflict keep both entries.
- `RECOVERY.md` and `PROJECT_CONTEXT.md`: updated by the coordinator at merge time.

## Interface changes

The signatures and response shapes in `API_CONTRACT.md` and `DATABASE_SCHEMA.md` are frozen. To change one, open a `chore/contract-<topic>` PR that updates the docs, the code stubs and `tests/test_foundation_contracts.py` together. All four areas must be told before it merges.

## Dependencies between areas

- Areas 2 and 3 are independent of everything else. They need only the frozen interfaces and their own test fixtures.
- Area 1 should merge first or early, since Area 4's orchestration needs `HistoricalTicket` and `get_db`. Until it merges, Area 4 tests `resolve_issue` with a fake session or monkeypatched helpers.
- Area 4 integrates last: it wires real retrieval and LLM modules once they have merged.

## Branch strategy

- `main` is always runnable and only receives merged PRs. Nobody commits to `main` directly. Recommended: enable branch protection requiring one approving review.
- Foundation branch: `chore/project-foundation` (this PR). Feature branches are the ones in the table. Other chores: `chore/<topic>`, fixes: `fix/<topic>`.
- Branch from the latest `main`. Before opening a PR run `git fetch origin && git rebase origin/main`, then `pytest -q`.
- One PR per area per milestone, targeting `main`. No force-pushes to shared branches. Only the coordinator merges.
- Commits are small and use a prefix: `feat:`, `fix:`, `chore:`, `docs:`, `test:`.
- Never commit `.env`, API keys, `tickets.db` or other generated files.
