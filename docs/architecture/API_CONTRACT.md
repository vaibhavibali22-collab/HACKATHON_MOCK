# API and Service Contract (FROZEN)

Status: frozen by the foundation PR. Any change requires a PR that updates this file and the
guard tests in `tests/test_foundation_contracts.py`, approved by the coordinator (Vaibhavi).

## 1. Shared constants (`app/config.py`)

| Name | Value | Meaning |
|---|---|---|
| `MIN_ISSUE_DESCRIPTION_LENGTH` | 10 | min characters after stripping whitespace |
| `MAX_ISSUE_DESCRIPTION_LENGTH` | 2000 | max characters after stripping whitespace |
| `DEFAULT_TOP_K` | 5 | retrieval result count used by `/resolve` |
| `RESOLUTION_STEP_COUNT` | 5 | exact step count on success |
| `MAX_STEP_LENGTH` | 500 | max characters per step |
| `MAX_LIST_LIMIT` | 200 | max `limit` for `GET /tickets` |
| `GENERATION_STATUS_*` | `success`, `insufficient_evidence`, `generation_failed` | the only legal `generation_status` values |

## 2. Service interfaces

### 2.1 `retrieve_similar_tickets(issue_description, tickets, top_k=5)` in `app/services/retrieval.py`

- **Input**
  - `issue_description: str`, already validated.
  - `tickets: Sequence[Mapping]`, plain dicts with keys `id`, `title`, `description`, `category`, `resolution`. ORM objects are NOT passed.
  - `top_k: int`, must be >= 1, otherwise `ValueError`.
- **Output**: `list[dict]`, at most `top_k` items. Each item has exactly: `ticket_id`, `title`, `description`, `category`, `resolution`, `similarity_score`.
  - `ticket_id` = the input record's `id`.
  - `similarity_score`: float in [0, 1], rounded to 4 decimals (cosine similarity on TF-IDF vectors).
  - Sorted by descending `similarity_score`; ties by ascending `ticket_id`.
  - Tickets scoring 0.0 are excluded. Empty `tickets` returns `[]`.
- Pure function: no database, no network, no global state that leaks between calls.

### 2.2 `generate_resolution_steps(issue_description, matched_tickets)` in `app/services/llm_service.py`

- **Input**: validated issue text; `matched_tickets` = the dicts produced by 2.1.
- **Output on success**: `list[str]` of exactly 5 strings, each non-empty after stripping, at most 500 characters, with leading numbering such as `1.` or `Step 1:` removed.
- **Errors** (raised, never swallowed, never replaced by made-up steps):

| Exception | When |
|---|---|
| `LLMServiceError` | base class |
| `LLMConfigurationError` | `GROQ_API_KEY` or `GROQ_MODEL` empty, or the configured model is not available to the key |
| `LLMUpstreamError` | timeout, connection error, rate limit, non-2xx from Groq |
| `LLMInvalidResponseError` | output is not parseable or does not validate as exactly five strings |

- The model ID comes only from `GROQ_MODEL`. There is no default model in code.
- Retrying is allowed inside the function, but a final failure must raise.

### 2.3 `resolve_issue(db, issue_description)` in `app/services/resolution_service.py`

- `db`: SQLAlchemy `Session`. `issue_description`: already validated by the API layer.
- Returns a dict identical in shape to the `POST /resolve` response (section 3.4).
- Algorithm:
  1. Load `HistoricalTicket` rows, convert to dicts (`id`, `title`, `description`, `category`, `resolution`).
  2. `retrieve_similar_tickets(..., top_k=5)`.
  3. **Relevance assessment**: if the list is empty, or the top `similarity_score` is below `RELEVANCE_THRESHOLD` (default `0.10`), return `insufficient_evidence` without calling the LLM.
  4. `generate_resolution_steps(...)`. On `LLMServiceError`, return `generation_failed`.
  5. Build the response.
- `LLMServiceError` is handled inside `resolve_issue`. Other exceptions (for example a database failure) propagate and become HTTP 500.

## 3. HTTP endpoints

Base URL: `API_BASE_URL` (default `http://localhost:8000`). JSON only. Timestamps are UTC, ISO 8601 with a trailing `Z`.

### 3.1 `GET /health`

`200` -> `{"status": "ok"}`. No database access required.

### 3.2 `GET /tickets?limit=50`

- `limit`: integer, default 50, min 1, max 200. Out of range or non-integer -> `422`.
- `200` -> `{"tickets": [Ticket, ...]}`, real stored rows, newest first (`id` descending).

`Ticket`:

```json
{
  "id": 1,
  "title": "string",
  "description": "string",
  "category": "string",
  "resolution": "string",
  "status": "resolved",
  "created_at": "2026-10-10T12:00:00Z"
}
```

### 3.3 `POST /tickets`

Request:

```json
{"title": "...", "description": "...", "category": "...", "resolution": "...", "status": "resolved"}
```

| Field | Rule |
|---|---|
| `title` | required, 1-200 chars after strip |
| `description` | required, 1-5000 chars after strip |
| `category` | required, 1-100 chars after strip |
| `resolution` | required, 1-5000 chars after strip |
| `status` | optional, 1-50 chars, default `"resolved"` |

Unknown fields are rejected. Success: `201` -> the stored `Ticket` (with its real `id` and `created_at`). Validation failure: `422`. The ticket is persisted before the response is sent.

### 3.4 `POST /resolve`

Request: `{"issue_description": "..."}`

Validation (FastAPI/Pydantic, `422` on failure):
- must be a string; leading/trailing whitespace is stripped before checks
- after stripping: at least 10 and at most 2000 characters
- the stripped value is what gets processed and echoed back in `issue_description`
- unknown fields are rejected

Response (always `200` when validation passes, including the two non-success statuses):

```json
{
  "issue_description": "...",
  "resolution_steps": ["...", "...", "...", "...", "..."],
  "matched_tickets": [
    {"ticket_id": 1, "title": "...", "category": "...", "similarity_score": 0.42}
  ],
  "generation_status": "success",
  "message": null
}
```

| `generation_status` | `resolution_steps` | `matched_tickets` | `message` |
|---|---|---|---|
| `success` | exactly 5 strings | 1-5 real retrieved tickets | `null` |
| `insufficient_evidence` | `[]` | whatever was actually retrieved (may be `[]`) | non-empty explanation |
| `generation_failed` | `[]` | the tickets that were retrieved | non-empty, user-safe explanation |

Rules:
- `matched_tickets` entries carry only `ticket_id`, `title`, `category`, `similarity_score`, sorted by descending score.
- Scores and ids always come from real retrieval. Never invent, pad or reorder evidence.
- `message` must not leak API keys, stack traces or raw upstream payloads.
- Never report `success` with a number of steps other than 5.

### 3.5 Error shapes

| Case | Status | Body |
|---|---|---|
| Validation error | 422 | FastAPI default `{"detail": [...]}` |
| Unexpected server error (for example database down) | 500 | `{"detail": "Internal server error"}` |

## 4. Environment variables

| Name | Default | Notes |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./tickets.db` | local SQLite file in the repo root, git-ignored |
| `GROQ_API_KEY` | empty | secret, never committed |
| `GROQ_MODEL` | empty | required for live generation; must be a model currently available to your tier |
| `GROQ_TIMEOUT_SECONDS` | `30` | per-request timeout |
| `API_BASE_URL` | `http://localhost:8000` | used by the Streamlit frontend |
| `RELEVANCE_THRESHOLD` | `0.10` | top-1 similarity floor; untuned starting value, tune against seeded data |
