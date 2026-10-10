# Architecture

## 1. Logical architecture

```
 Streamlit UI  --HTTP/JSON-->  FastAPI (app/api)  -->  resolve_issue (services/resolution_service)
 frontend/                      routes + schemas          |            |             |
                                                          v            v             v
                                                   SQLAlchemy/SQLite   retrieval     llm_service
                                                   (app/db)            (TF-IDF,      (Groq API,
                                                                       cosine)       model from env)
```

Layers and rules:
- **Frontend** talks to the backend only over HTTP at `API_BASE_URL`. It never imports from `app/`.
- **API layer** validates input, calls services, shapes responses. No business logic, no SQL.
- **Orchestration** (`resolve_issue`) is the only code that connects retrieval and generation.
- **Retrieval** is a pure function over dicts. It knows nothing about the database or the LLM.
- **LLM service** knows nothing about the database or retrieval internals. It receives dicts and returns five strings or raises.
- **DB layer** owns models, sessions and seeding.

Because the services depend only on the frozen interfaces in `API_CONTRACT.md`, the four areas can be built and tested independently, using fake dicts and mocks.

## 2. Request processing: `POST /resolve`

1. Pydantic validates the body (strip, 10-2000 chars). Failure -> `422`.
2. The route gets a DB session through `get_db` and calls `resolve_issue(db, issue_description)`.
3. `resolve_issue` loads all `historical_tickets` and converts them to dicts.
4. `retrieve_similar_tickets(issue, tickets, top_k=5)` returns up to 5 scored tickets.
5. Relevance check: no results, or top score < `RELEVANCE_THRESHOLD` -> return `insufficient_evidence` (no LLM call).
6. `generate_resolution_steps(issue, matched)` returns exactly 5 strings.
7. Build the response: five steps, matched tickets reduced to `ticket_id`, `title`, `category`, `similarity_score`, `generation_status="success"`, `message=null`.
8. The route returns `200` with that body.

## 3. Failure paths

| Failure | Detected in | Result |
|---|---|---|
| Missing/short/long/non-string input | API validation | `422`, nothing else runs |
| Empty database, or no ticket scores above 0 | retrieval returns `[]` | `200`, `insufficient_evidence`, steps `[]` |
| Best score below `RELEVANCE_THRESHOLD` | `resolve_issue` | `200`, `insufficient_evidence`, retrieved tickets listed, steps `[]` |
| `GROQ_API_KEY` / `GROQ_MODEL` unset, or model unavailable | `llm_service` -> `LLMConfigurationError` | `200`, `generation_failed`, safe message |
| Groq timeout / network / rate limit / HTTP error | `LLMUpstreamError` | `200`, `generation_failed` |
| Model output is not exactly five valid strings | `LLMInvalidResponseError` | `200`, `generation_failed` |
| Database error or any unexpected exception | anywhere else | `500 {"detail": "Internal server error"}`, details logged server-side only |
| Backend down (seen from the UI) | Streamlit | UI shows a connection error; it never shows fabricated steps |

Principles: never return fabricated steps or evidence; never report `success` unless exactly 5 validated steps exist; never expose secrets or stack traces in `message`.

## 4. Startup commands

Prerequisite: Python 3.11+ recommended (the foundation was verified on 3.13).

```bash
git clone https://github.com/vaibhavibali22-collab/hackathon_mock.git
cd hackathon_mock
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                 # then edit .env: set GROQ_API_KEY and GROQ_MODEL

python -m app.db.seed                # idempotent; available once Area 1 is merged
uvicorn app.main:app --reload --port 8000     # backend; available once Area 4 is merged
streamlit run frontend/streamlit_app.py       # frontend (second terminal)
pytest -q                            # tests
```

Health check: `curl http://localhost:8000/health` -> `{"status":"ok"}`.

Until the feature PRs merge, only `pytest -q` is expected to work; `app.main`, the seed script and the UI are placeholders.

## 5. Structure deviations from the suggested layout

- Added `__init__.py` files so `app`, `app.api`, `app.db`, `app.services`, `tests` are importable packages.
- Added `.gitkeep` in `data/` and `docs/learning/` so the folders exist before content does.
- `app/config.py` is implemented (not a placeholder) because every area depends on its constants and env var names.
- The three service modules contain the frozen signatures, docstrings and (for the LLM service) the exception classes, with bodies that raise `NotImplementedError`.
- Added `tests/test_foundation_contracts.py` to guard signatures, constants and env var names.
- `data/synthetic_tickets.json` is intentionally not created here; it belongs to Area 1.
