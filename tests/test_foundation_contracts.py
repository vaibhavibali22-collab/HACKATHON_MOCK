"""Guards the frozen foundation contracts. If one of these fails, a contract was changed:
that requires a PR that also updates docs/architecture/ and is approved by the coordinator."""
import inspect

import pytest

from app import config
from app.services import llm_service, resolution_service, retrieval


def _params(fn):
    return [(p.name, p.default) for p in inspect.signature(fn).parameters.values()]


def test_retrieval_signature_is_frozen():
    assert _params(retrieval.retrieve_similar_tickets) == [
        ("issue_description", inspect.Parameter.empty),
        ("tickets", inspect.Parameter.empty),
        ("top_k", 5),
    ]


def test_llm_signature_is_frozen():
    assert _params(llm_service.generate_resolution_steps) == [
        ("issue_description", inspect.Parameter.empty),
        ("matched_tickets", inspect.Parameter.empty),
    ]


def test_resolve_issue_signature_is_frozen():
    assert _params(resolution_service.resolve_issue) == [
        ("db", inspect.Parameter.empty),
        ("issue_description", inspect.Parameter.empty),
    ]


def test_llm_error_hierarchy_is_frozen():
    for sub in (
        llm_service.LLMConfigurationError,
        llm_service.LLMUpstreamError,
        llm_service.LLMInvalidResponseError,
    ):
        assert issubclass(sub, llm_service.LLMServiceError)


def test_shared_constants_are_frozen():
    assert config.MIN_ISSUE_DESCRIPTION_LENGTH == 10
    assert config.MAX_ISSUE_DESCRIPTION_LENGTH == 2000
    assert config.DEFAULT_TOP_K == 5
    assert config.RESOLUTION_STEP_COUNT == 5
    assert config.MAX_STEP_LENGTH == 500
    assert config.GENERATION_STATUS_SUCCESS == "success"
    assert config.GENERATION_STATUS_INSUFFICIENT_EVIDENCE == "insufficient_evidence"
    assert config.GENERATION_STATUS_FAILED == "generation_failed"


ENV_VARS = (
    "DATABASE_URL",
    "GROQ_API_KEY",
    "GROQ_MODEL",
    "GROQ_TIMEOUT_SECONDS",
    "API_BASE_URL",
    "RELEVANCE_THRESHOLD",
)


def test_settings_defaults(monkeypatch):
    for name in ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    s = config.get_settings()
    assert s.database_url == "sqlite:///./tickets.db"
    assert s.groq_api_key == ""
    assert s.groq_model == ""  # no hard-coded model ID
    assert s.api_base_url == "http://localhost:8000"
    assert s.relevance_threshold == pytest.approx(0.10)


def test_settings_read_env_each_call(monkeypatch):
    monkeypatch.setenv("GROQ_MODEL", "example-model-id")
    monkeypatch.setenv("RELEVANCE_THRESHOLD", "0.25")
    s = config.get_settings()
    assert s.groq_model == "example-model-id"
    assert s.relevance_threshold == pytest.approx(0.25)


@pytest.mark.parametrize("value", ["abc", "-0.1", "1.5"])
def test_invalid_relevance_threshold_rejected(monkeypatch, value):
    monkeypatch.setenv("RELEVANCE_THRESHOLD", value)
    with pytest.raises(ValueError, match="RELEVANCE_THRESHOLD"):
        config.get_settings()


def test_env_example_lists_every_env_var():
    from pathlib import Path

    text = (Path(__file__).resolve().parents[1] / ".env.example").read_text()
    for name in ENV_VARS:
        assert f"{name}=" in text
