"""Built-in model-provider registry.

Hosted entries use the OpenAI-compatible chat/embedding contract. Credentials are
read from environment variables and are never included in status output.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProviderSpec:
    id: str
    display_name: str
    kind: str
    default_base_url: str | None
    api_key_env: str | None
    default_chat_model: str | None
    default_embedding_model: str | None
    cli_model: str | None
    notes: str


PROVIDERS: tuple[ProviderSpec, ...] = (
    ProviderSpec("extractive", "Local extractive", "local", None, None, None, None, None,
                 "No network or API key; returns cited retrieved excerpts."),
    ProviderSpec("openai", "OpenAI", "openai-compatible", "https://api.openai.com/v1",
                 "OPENAI_API_KEY", "gpt-4.1-mini", "text-embedding-3-small", "openai/gpt-4.1-mini",
                 "OpenAI-compatible chat and embedding APIs."),
    ProviderSpec("zai", "Z.ai (GLM)", "openai-compatible", "https://api.z.ai/api/paas/v4",
                 "ZAI_API_KEY", "glm-5.3", None, "zai/glm-5.3",
                 "GLM chat API; configure a compatible embedding endpoint separately."),
    ProviderSpec("deepseek", "DeepSeek", "openai-compatible", "https://api.deepseek.com/v1",
                 "DEEPSEEK_API_KEY", "deepseek-v4-pro", None, "deepseek/deepseek-v4-pro",
                 "DeepSeek chat API; embedding support depends on the selected endpoint."),
    ProviderSpec("orcarouter", "OrcaRouter", "openai-compatible", None, "ORCAROUTER_API_KEY",
                 "orcarouter/free", None, "orcarouter/free",
                 "Set REDOPS_ORCAROUTER_BASE_URL to the configured OrcaRouter endpoint."),
)

_BY_ID = {spec.id: spec for spec in PROVIDERS}


def provider_ids() -> tuple[str, ...]:
    return tuple(spec.id for spec in PROVIDERS)


def get_provider(provider_id: str) -> ProviderSpec:
    normalized = provider_id.strip().lower()
    try:
        return _BY_ID[normalized]
    except KeyError as exc:
        supported = ", ".join(provider_ids())
        raise ValueError(f"unsupported provider '{provider_id}'; choose one of: {supported}") from exc
