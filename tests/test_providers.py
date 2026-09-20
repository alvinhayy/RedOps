from redops_rag.config import Settings
from redops_rag.providers import get_provider, provider_ids


def test_provider_registry_contains_opencode_providers():
    assert {"zai", "deepseek", "orcarouter"}.issubset(provider_ids())
    assert get_provider("ZAI").default_chat_model == "glm-5.3"


def test_provider_specific_credentials_and_base_url(monkeypatch):
    monkeypatch.setenv("REDOPS_LLM_PROVIDER", "deepseek")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-secret")
    monkeypatch.delenv("REDOPS_API_KEY", raising=False)
    settings = Settings.from_env()
    assert settings.api_key == "test-secret"
    assert settings.api_base_url == "https://api.deepseek.com/v1"
    assert settings.llm_model == "deepseek-v4-pro"


def test_provider_override_wins(monkeypatch):
    monkeypatch.setenv("REDOPS_LLM_PROVIDER", "orcarouter")
    monkeypatch.setenv("ORCAROUTER_API_KEY", "test-secret")
    monkeypatch.setenv("REDOPS_ORCAROUTER_BASE_URL", "http://127.0.0.1:9999/v1")
    settings = Settings.from_env()
    assert settings.api_base_url == "http://127.0.0.1:9999/v1"
    assert settings.api_key == "test-secret"
