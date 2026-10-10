# Database Schema (FROZEN)

Engine: SQLAlchemy 2.x. Default store: SQLite file `./tickets.db` (git-ignored). MVP has no migrations; tables are created with `Base.metadata.create_all(engine)` through `init_db()` on app startup and in the seed script.

## Table `historical_tickets` (model `HistoricalTicket`)

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | Integer | primary key, autoincrement | exposed as `id` in the API and as `ticket_id` in retrieval output |
| `title` | String(200) | not null | |
| `description` | Text | not null | |
| `category` | String(100) | not null | |
| `resolution` | Text | not null | the known fix; the LLM is grounded on this |
| `status` | String(50) | not null, default `"resolved"` | |
| `created_at` | DateTime | not null, default = current UTC time | stored as naive UTC; serialised as ISO 8601 with `Z` |

Frozen exports of `app/db/database.py`: `Base`, `engine`, `SessionLocal`, `get_db` (FastAPI dependency yielding a Session and always closing it), `init_db`.
Frozen export of `app/db/models.py`: `HistoricalTicket`, with `__tablename__ = "historical_tickets"`.

## Seeding

- Source: `data/synthetic_tickets.json`, a JSON array of objects with `title`, `description`, `category`, `resolution` and optional `status`. All data is synthetic; no real customer or company information.
- Command: `python -m app.db.seed`
- **Idempotent**: a record is inserted only if no existing row has the same `title` and `category`. Running the seed N times leaves the same row count as running it once. It never deletes or updates existing rows.
- The seed prints how many rows were inserted and how many were skipped.
- Resetting a local database: stop the backend, delete `tickets.db`, run the seed again.
