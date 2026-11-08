"""Typed configuration with secret masking.

Secrets are read only from environment variables (or a git-ignored ``.env``),
never from YAML, and are wrapped in ``SecretStr`` so they do not appear in
``repr`` or serialized output.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field, SecretStr

DEFAULT_CONFIG_PATH = Path("config/default.yaml")
API_KEY_ENV = "ANTHROPIC_API_KEY"


class Paths(BaseModel):
    model_config = ConfigDict(frozen=True)

    raw: Path = Path("data/raw")
    interim: Path = Path("data/interim")
    features: Path = Path("data/features")
    labeled: Path = Path("data/labeled")
    outputs: Path = Path("data/outputs")


class LLMSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    small_model: str = "claude-haiku-5-5"
    large_model: str = "claude-sonnet-5-5"
    temperature: float = 0.0
    max_attempts: int = Field(default=3, ge=1)
    budget_usd: float = Field(default=0.0, ge=0.0)
    api_key: SecretStr | None = None


class LoggingSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    level: str = "INFO"


class Settings(BaseModel):
    model_config = ConfigDict(frozen=True)

    seed: int = 20260101
    paths: Paths = Paths()
    llm: LLMSettings = LLMSettings()
    logging: LoggingSettings = LoggingSettings()

    def component_seed(self, component: str) -> int:
        """Stable per-component seed derived from the master seed."""
        digest = hashlib.sha256(f"{self.seed}:{component}".encode()).digest()
        return int.from_bytes(digest[:4], "big")


def load_settings(path: Path | None = None, *, env_file: Path | None = None) -> Settings:
    """Load YAML defaults, then overlay secrets from the environment."""
    load_dotenv(env_file, override=False)
    config_path = path or DEFAULT_CONFIG_PATH
    raw: dict[str, object] = {}
    if config_path.exists():
        loaded = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        raw = loaded if isinstance(loaded, dict) else {}
    llm = dict(raw.get("llm") or {})  # type: ignore[call-overload]
    llm.pop("api_key", None)  # secrets are never accepted from files
    key = os.environ.get(API_KEY_ENV)
    if key:
        llm["api_key"] = key
    raw["llm"] = llm
    return Settings.model_validate(raw)
