# Project Context (authoritative)

If another document disagrees with this one or with `docs/architecture/`, those win; fix the other document.

## Purpose

IT Ticket Resolution Suggestion Engine, built for a hackathon by a team of four. Repository owner and integration coordinator: Vaibhavi.

## Stack

Streamlit (frontend), FastAPI (backend), SQLAlchemy + SQLite (storage), scikit-learn TF-IDF + cosine similarity (retrieval), Groq API (generation, model chosen by `GROQ_MODEL`).

## Architecture in one paragraph

The UI calls `POST /resolve` on the FastAPI backend. `resolve_issue(db, issue_description)` loads historical tickets, calls `retrieve_similar_tickets` (top 5), checks relevance against `RELEVANCE_THRESHOLD`, then calls `generate_resolution_steps`. Success means exactly five validated steps plus the real matched tickets. Weak evidence returns `insufficient_evidence`; Groq or validation problems return `generation_failed`; neither fabricates anything. Details: `docs/architecture/ARCHITECTURE.md`.

## Frozen decisions

| Topic | Decision | Where |
|---|---|---|
| Table | `historical_tickets`: `id`, `title`, `description`, `category`, `resolution`, `status` (default `resolved`), `created_at` | DATABASE_SCHEMA.md |
| Seeding | idempotent, keyed on `title` + `category` | DATABASE_SCHEMA.md |
| Retrieval | `retrieve_similar_tickets(issue_description, tickets, top_k=5)` over dicts, returns scored dicts | API_CONTRACT.md 2.1 |
| LLM | `generate_resolution_steps(issue_description, matched_tickets)` returns exactly 5 strings or raises `LLMServiceError` subclasses | API_CONTRACT.md 2.2 |
| Orchestration | `resolve_issue(db, issue_description)` | API_CONTRACT.md 2.3 |
| Endpoints | `GET /health`, `GET /tickets?limit=50`, `POST /tickets`, `POST /resolve` | API_CONTRACT.md 3 |
| Input limits | issue text 10-2000 chars after strip; `limit` 1-200 | API_CONTRACT.md 1, 3 |
| Statuses | `success`, `insufficient_evidence`, `generation_failed` | API_CONTRACT.md 3.4 |
| Relevance threshold | `RELEVANCE_THRESHOLD`, default 0.10, untuned | API_CONTRACT.md 4 |
| Groq model | configured only via `GROQ_MODEL`; no default; must be verified available | CONTRIBUTING.md |

## Ownership

Four areas (Data layer, Retrieval, LLM service, API/orchestration/frontend), each on its own branch, with shared files controlled by the coordinator. See `docs/architecture/OWNERSHIP.md`.

## Deviations from the suggested layout

Listed in `docs/architecture/ARCHITECTURE.md` section 5.

## Continuity files

- `PROJECT_CONTEXT.md` (this file): architecture and decisions.
- `IMPLEMENTATION_LOG.md`: chronological record.
- `RECOVERY.md`: last verified state and next safe task.
- `TASK_TRACKER.md`: task status per area.
