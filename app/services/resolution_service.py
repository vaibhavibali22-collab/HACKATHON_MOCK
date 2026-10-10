"""Resolution orchestration.

Owner: Area 4 (API, orchestration & frontend). FROZEN INTERFACE; implement the body,
do not change the signature or the response keys.
Contract: docs/architecture/API_CONTRACT.md ("POST /resolve" and "Service interfaces").
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def resolve_issue(db: "Session", issue_description: str) -> dict[str, Any]:
    """Coordinate retrieval, relevance assessment, generation and response construction.

    Steps (see docs/architecture/ARCHITECTURE.md for the failure paths):
      1. Load HistoricalTicket rows and convert them to plain dicts (``id``, ``title``, ...).
      2. ``retrieve_similar_tickets(issue_description, tickets, top_k=5)``.
      3. Relevance check: no matches, or top similarity_score < settings.relevance_threshold
         -> generation_status "insufficient_evidence" (the LLM is NOT called).
      4. ``generate_resolution_steps(issue_description, matched_tickets)``;
         LLMServiceError -> generation_status "generation_failed".
      5. Build the response dict.

    Returns a JSON-serialisable dict with exactly the keys: ``issue_description``,
    ``resolution_steps``, ``matched_tickets`` (each with only ``ticket_id``, ``title``,
    ``category``, ``similarity_score``), ``generation_status``, ``message``.
    Success => exactly 5 steps and ``message`` is None. Any other status => ``resolution_steps``
    is [] and ``message`` is a non-empty explanation.
    LLMServiceError is handled here; unexpected errors (e.g. database failure) propagate.
    """
    raise NotImplementedError("Area 4 implements this.")
