"""Central configuration: the single source of truth for env-var names and shared constants.

Owner: integration coordinator (shared file). Change only via PR.
Contract reference: docs/architecture/API_CONTRACT.md, docs/architecture/ARCHITECTURE.md
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

# --- Frozen shared constants (changing any of these is a contract change) ---
MIN_ISSUE_DESCRIPTION_LENGTH = 10  # characters, after stripping whitespace
MAX_ISSUE_DESCRIPTION_LENGTH = 2000  # characters, after stripping whitespace
DEFAULT_TOP_K = 5
RESOLUTION_STEP_COUNT = 5
MAX_STEP_LENGTH = 500  # characters per resolution step
MAX_LIST_LIMIT = 200  # upper bound for GET /tickets?limit=

GENERATION_STATUS_SUCCESS = "success"
GENERATION_STATUS_INSUFFICIENT_EVIDENCE = "insufficient_evidence"
GENERATION_STATUS_FAILED = "generation_failed"

DEFAULT_DATABASE_URL = "sqlite:///./tickets.db"
DEFAULT_API_BASE_URL = "http://localhost:8000"
DEFAULT_RELEVANCE_THRESHOLD = 0.10
DEFAULT_GROQ_TIMEOUT_SECONDS = 30.0


@dataclass(frozen=True)
class Settings:
    database_url: str
    groq_api_key: str
    groq_model: str  # empty string means "not configured"; the LLM service must raise LLMConfigurationError
    groq_timeout_seconds: float
    api_base_url: str
    relevance_threshold: float


def _float_env(name: str, default: float, lo: float, hi: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be a number, got {raw!r}") from exc
    if not lo <= value <= hi:
        raise ValueError(f"{name} must be between {lo} and {hi}, got {value}")
    return value


def get_settings() -> Settings:
    """Read settings from the environment on every call (so tests can monkeypatch env vars)."""
    return Settings(
        database_url=os.getenv("DATABASE_URL") or DEFAULT_DATABASE_URL,
        groq_api_key=os.getenv("GROQ_API_KEY", ""),
        groq_model=os.getenv("GROQ_MODEL", ""),
        groq_timeout_seconds=_float_env("GROQ_TIMEOUT_SECONDS", DEFAULT_GROQ_TIMEOUT_SECONDS, 1.0, 300.0),
        api_base_url=os.getenv("API_BASE_URL") or DEFAULT_API_BASE_URL,
        relevance_threshold=_float_env("RELEVANCE_THRESHOLD", DEFAULT_RELEVANCE_THRESHOLD, 0.0, 1.0),
    )
