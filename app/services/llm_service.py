"""LLM service (Groq).

Owner: Area 3 (LLM). FROZEN INTERFACE; implement the body, do not change the signature
or the exception hierarchy.
Contract: docs/architecture/API_CONTRACT.md ("Service interfaces").
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


class LLMServiceError(Exception):
    """Base class. Raised instead of ever returning fabricated or partial steps."""


class LLMConfigurationError(LLMServiceError):
    """GROQ_API_KEY or GROQ_MODEL missing/empty, or the configured model is unavailable."""


class LLMUpstreamError(LLMServiceError):
    """Groq API unreachable, timed out, rate limited, or returned an error status."""


class LLMInvalidResponseError(LLMServiceError):
    """Model output could not be validated as exactly five non-empty, actionable strings."""


def generate_resolution_steps(
    issue_description: str,
    matched_tickets: Sequence[Mapping[str, Any]],
) -> list[str]:
    """Generate resolution steps grounded in ``matched_tickets``.

    Input:
        issue_description: validated issue text.
        matched_tickets: dicts as returned by ``retrieve_similar_tickets``.

    Output: exactly ``RESOLUTION_STEP_COUNT`` (5) strings; each non-empty after stripping,
    at most ``MAX_STEP_LENGTH`` (500) characters. Leading numbering ("1.", "Step 1:") is stripped.

    Raises: ``LLMServiceError`` (or a subclass) on ANY failure. Never returns fewer or more
    than five steps, never returns placeholder text.
    """
    raise NotImplementedError("Area 3 (LLM) implements this.")
