# HACKATHON_MOCK

IT Ticket Resolution Suggestion Engine. A user describes an IT issue; the system finds similar resolved tickets (TF-IDF + cosine similarity) and asks an LLM (Groq) for exactly five actionable resolution steps grounded in those tickets. If the evidence is weak or generation fails, it says so instead of making something up.

**Stack:** Streamlit (UI), FastAPI (API), SQLAlchemy + SQLite (data), scikit-learn (retrieval), Groq API (generation).

**Status:** foundation and contracts only. Feature work has not started. See [TASK_TRACKER.md](TASK_TRACKER.md).

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                 # set GROQ_API_KEY and GROQ_MODEL
pytest -q                            # works today (contract tests)

# Available after the feature PRs merge:
python -m app.db.seed                # load synthetic tickets (idempotent)
uvicorn app.main:app --reload --port 8000
streamlit run frontend/streamlit_app.py
```

`GROQ_MODEL` has no default. Choose a model that is currently available to your API tier (see the comment in `.env.example`).

## Where to read next

| File | Purpose |
|---|---|
| [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) | authoritative architecture and decisions |
| [docs/architecture/API_CONTRACT.md](docs/architecture/API_CONTRACT.md) | frozen service and HTTP contracts |
| [docs/architecture/DATABASE_SCHEMA.md](docs/architecture/DATABASE_SCHEMA.md) | table, seeding rules |
| [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) | layers, request flow, failure paths, startup |
| [docs/architecture/OWNERSHIP.md](docs/architecture/OWNERSHIP.md) | who edits what, branch strategy |
| [CONTRIBUTING.md](CONTRIBUTING.md) | workflow rules |
| [TASK_TRACKER.md](TASK_TRACKER.md), [IMPLEMENTATION_LOG.md](IMPLEMENTATION_LOG.md), [RECOVERY.md](RECOVERY.md) | status, history, how to resume |

Repository owner and integration coordinator: Vaibhavi.
