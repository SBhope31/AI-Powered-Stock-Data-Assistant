from dataclasses import dataclass
import os
from dotenv import load_dotenv
load_dotenv()

@dataclass(frozen=True)
class Config:
    api_key: str
    base_url: str
    model: str
    request_timeout_seconds: int = 30


def load_config() -> Config:
    github_token = os.getenv("GIT_ACCESS_TOKEN", "").strip()
    github_base_url = os.getenv("GITHUB_MODELS_BASE_URL", "").strip()
    github_model = os.getenv("GITHUB_MODELS_MODEL", "").strip()

    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    openai_base_url = os.getenv("OPENAI_BASE_URL", "").strip()
    openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

    if github_token:
        base_url = github_base_url or "https://models.github.ai/inference"
        model = github_model or "openai/gpt-4o-mini"
        return Config(api_key=github_token, base_url=base_url, model=model)

    if openai_key:
        return Config(api_key=openai_key, base_url=openai_base_url, model=openai_model)

    raise ValueError(
        "Missing API key. Set GIT_ACCESS_TOKEN (GitHub Models) or OPENAI_API_KEY."
    )
