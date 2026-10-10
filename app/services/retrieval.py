"""Retrieval service (TF-IDF + cosine similarity).

Owner: Area 2 (Retrieval). FROZEN INTERFACE; implement the body, do not change the signature.
Contract: docs/architecture/API_CONTRACT.md ("Service interfaces").
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


def retrieve_similar_tickets(
    issue_description: str,
    tickets: Sequence[Mapping[str, Any]],
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """Return up to ``top_k`` historical tickets most similar to ``issue_description``.

    Input:
        issue_description: already-validated text (see config MIN/MAX_ISSUE_DESCRIPTION_LENGTH).
        tickets: sequence of mappings with keys ``id``, ``title``, ``description``,
            ``category``, ``resolution``. Plain dicts, NOT ORM objects.
        top_k: maximum number of results; must be >= 1 (ValueError otherwise).

    Output: list of dicts with exactly the keys ``ticket_id``, ``title``, ``description``,
    ``category``, ``resolution``, ``similarity_score`` (float in [0, 1], rounded to 4 places),
    sorted by descending ``similarity_score``; ties broken by ascending ``ticket_id``.
    Tickets with a score of 0.0 are excluded. Empty ``tickets`` returns ``[]``.
    """
    raise NotImplementedError("Area 2 (Retrieval) implements this.")
