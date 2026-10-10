# Task Tracker

Each area edits only its own section. Update the status when it changes and be honest about it.

## Status legend

| Status | Meaning |
|---|---|
| NOT STARTED | no work yet |
| IN PROGRESS | being worked on |
| BLOCKED | cannot proceed; say what blocks it |
| IMPLEMENTED — NOT VERIFIED | code written, but not run or tested end to end |
| VERIFIED | run and checked; say how in the Notes column |
| DEFERRED | intentionally postponed |

## Foundation (coordinator)

| Task | Status | Notes |
|---|---|---|
| Directory layout, placeholders, ownership plan | IMPLEMENTED — NOT VERIFIED | awaiting review/merge of `chore/project-foundation` |
| Frozen contracts and architecture docs | IMPLEMENTED — NOT VERIFIED | awaiting coordinator review |
| `app/config.py`, `.env.example`, `requirements.txt`, `.gitignore` | VERIFIED | `pip install -r requirements.txt` in a clean venv succeeded; `pytest -q`: 11 passed (2026-10-10) |
| Foundation PR merged to `main` | NOT STARTED | Vaibhavi |

## Area 1 — Data layer (owner: TBD, branch `feat/data-layer`)

| Task | Status | Notes |
|---|---|---|
| `database.py` (Base, engine, SessionLocal, get_db, init_db) | NOT STARTED | |
| `models.py` (`HistoricalTicket`) | NOT STARTED | |
| `data/synthetic_tickets.json` | NOT STARTED | synthetic only |
| `seed.py`, idempotent | NOT STARTED | |
| DB and seed tests | NOT STARTED | |

## Area 2 — Retrieval (owner: TBD, branch `feat/retrieval`)

| Task | Status | Notes |
|---|---|---|
| `retrieve_similar_tickets` (TF-IDF + cosine) | NOT STARTED | |
| Retrieval tests (ordering, top_k, empty input, zero scores) | NOT STARTED | |
| Calibrate `RELEVANCE_THRESHOLD` suggestion | NOT STARTED | report to coordinator |

## Area 3 — LLM service (owner: TBD, branch `feat/llm-service`)

| Task | Status | Notes |
|---|---|---|
| `generate_resolution_steps` (Groq) | NOT STARTED | |
| Output validation (exactly 5 steps) and error mapping | NOT STARTED | |
| Tests with mocked Groq client | NOT STARTED | |
| Live check: model availability + one real call | NOT STARTED | needs a real key; do not claim verified without it |

## Area 4 — API, orchestration and frontend (owner: TBD, branch `feat/api-orchestration-frontend`)

| Task | Status | Notes |
|---|---|---|
| `schemas.py`, `routes.py`, `main.py` | NOT STARTED | |
| `resolve_issue` orchestration | NOT STARTED | |
| API tests (validation, statuses, 422/500) | NOT STARTED | |
| Streamlit UI | NOT STARTED | |
| End-to-end run with all areas merged | NOT STARTED | |
