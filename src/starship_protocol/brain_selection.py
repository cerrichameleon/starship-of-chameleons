from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .providers import BrainSelectionResult


CONFIG_CANDIDATES = [
    Path.home() / ".openclaw" / "openclaw.json",
    Path("/home/node/.openclaw/openclaw.json"),
]
CREDENTIAL_FILE_NAMES = [
    Path("var/provider_credentials.json"),
    Path("provider_credentials.json"),
]
CODEX_AUTH_CANDIDATES = [
    Path(os.getenv("CODEX_HOME", "~/.codex")).expanduser() / "auth.json",
    Path.home() / ".codex" / "auth.json",
]


@dataclass
class LaunchPolicy:
    provider_order: list[str] = field(default_factory=list)


@dataclass
class BrainSelectionPolicy:
    preferred_providers: list[str] = field(
        default_factory=lambda: ["codex", "openai-api", "gemini-api"]
    )


def hydrate_known_credentials() -> dict[str, str]:
    hydrated: dict[str, str] = {}
    for key_name in ["OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"]:
        if os.getenv(key_name):
            hydrated[key_name] = os.environ[key_name]

    config_env = _load_config_env_vars()
    for key_name in ["OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"]:
        if key_name in hydrated:
            continue
        configured_value = config_env.get(key_name)
        if not configured_value:
            continue
        if configured_value.startswith("${") and configured_value.endswith("}"):
            referenced_name = configured_value[2:-1]
            if os.getenv(referenced_name):
                hydrated[key_name] = os.environ[referenced_name]
        else:
            hydrated[key_name] = configured_value

    file_env = _load_file_env_vars()
    for key_name in ["OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"]:
        if key_name not in hydrated and file_env.get(key_name):
            hydrated[key_name] = file_env[key_name]

    docker_env = _load_docker_env_vars()
    for key_name in ["OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"]:
        if key_name not in hydrated and docker_env.get(key_name):
            hydrated[key_name] = docker_env[key_name]

    for key_name, key_value in hydrated.items():
        os.environ[key_name] = key_value

    return hydrated


def detect_provider_readiness() -> dict[str, dict[str, Any]]:
    hydrated = hydrate_known_credentials()
    openai_key = hydrated.get("OPENAI_API_KEY")
    gemini_key = hydrated.get("GEMINI_API_KEY") or hydrated.get("GOOGLE_API_KEY")
    codex_ready = _codex_auth_available()

    return {
        "openai-api": {
            "status": "ready" if openai_key else "needs-setup",
            "severity": "green" if openai_key else "red",
            "ready": bool(openai_key),
            "detail": "API key detected and ready for launch." if openai_key else "No OpenAI API key detected yet.",
        },
        "codex-oauth": {
            "status": "ready" if codex_ready else "needs-human-login",
            "severity": "green" if codex_ready else "red",
            "ready": codex_ready,
            "detail": "Codex auth file detected for direct Starship use." if codex_ready else "No Codex auth file detected yet. Run codex login or codex login --device-auth first.",
        },
        "gemini-api": {
            "status": "ready" if gemini_key else "needs-setup",
            "severity": "green" if gemini_key else "red",
            "ready": bool(gemini_key),
            "detail": "Gemini API key detected and ready for launch." if gemini_key else "No Gemini API key detected yet.",
        },
    }


def select_brain_for_launch(policy: LaunchPolicy | None = None) -> BrainSelectionResult:
    hydrated = hydrate_known_credentials()
    attempt_log: list[str] = []

    openai_key = hydrated.get("OPENAI_API_KEY")
    gemini_key = hydrated.get("GEMINI_API_KEY") or hydrated.get("GOOGLE_API_KEY")
    gemini_credentials_ref = "env:GEMINI_API_KEY" if hydrated.get("GEMINI_API_KEY") else "env:GOOGLE_API_KEY"
    provider_order = [provider_id for provider_id in (policy.provider_order if policy else []) if provider_id]
    if not provider_order:
        provider_order = ["codex", "openai-api", "gemini-api"]
    attempt_log.append("provider order: " + ", ".join(provider_order))

    for provider_id in provider_order:
        if provider_id in {"codex", "codex-oauth"}:
            if _codex_auth_available():
                attempt_log.append("codex auth file detected, but direct Starship Codex runtime is not implemented yet")
            else:
                attempt_log.append("codex auth file unavailable")
            continue

        if provider_id == "openai-api":
            if openai_key:
                attempt_log.append("openai-api key available")
                return BrainSelectionResult(
                    provider_label="OpenAI",
                    model_label="gpt-5.4",
                    access_path="api-key",
                    credentials_ref="env:OPENAI_API_KEY",
                    launch_note="Using onboarding-aware OpenAI API launch path.",
                    using_tokens=True,
                    attempt_log=attempt_log,
                    provider_id="openai-api",
                )
            attempt_log.append("openai-api unavailable")
            continue

        if provider_id == "gemini-api":
            if gemini_key:
                attempt_log.append("gemini-api key available")
                return BrainSelectionResult(
                    provider_label="Google",
                    model_label="gemini-2.5-pro",
                    access_path="api-key",
                    credentials_ref=gemini_credentials_ref,
                    launch_note="Using onboarding-aware Gemini API launch path.",
                    using_tokens=True,
                    attempt_log=attempt_log,
                    provider_id="gemini-api",
                )
            attempt_log.append("gemini-api unavailable")
            continue

        attempt_log.append(f"unknown provider in launch policy: {provider_id}")

    return BrainSelectionResult(
        provider_label="unavailable",
        model_label="none",
        access_path="none",
        credentials_ref="none",
        launch_note="No real brain provider was available for launch.",
        using_tokens=False,
        attempt_log=attempt_log,
        provider_id="unavailable",
    )


def _load_config_env_vars() -> dict[str, str]:
    for candidate in CONFIG_CANDIDATES:
        if not candidate.exists():
            continue
        try:
            config = json.loads(candidate.read_text())
        except Exception:
            continue
        env_vars = config.get("env", {}).get("vars", {})
        if isinstance(env_vars, dict):
            return {str(key): str(value) for key, value in env_vars.items()}
    return {}


def _load_file_env_vars() -> dict[str, str]:
    candidate_from_env = os.getenv("STARSHIP_PROVIDER_CREDENTIALS_FILE")
    candidates: list[Path] = []
    if candidate_from_env:
        candidates.append(Path(candidate_from_env))
    cwd = Path.cwd()
    candidates.extend(cwd / relative_path for relative_path in CREDENTIAL_FILE_NAMES)

    seen: set[Path] = set()
    for candidate in candidates:
        resolved_candidate = candidate.resolve()
        if resolved_candidate in seen or not resolved_candidate.exists():
            continue
        seen.add(resolved_candidate)
        try:
            payload = json.loads(resolved_candidate.read_text())
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        return {
            str(key): str(value)
            for key, value in payload.items()
            if str(key) in {"OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"} and value
        }
    return {}


def _codex_auth_available() -> bool:
    for candidate in CODEX_AUTH_CANDIDATES:
        if not candidate.exists():
            continue
        try:
            payload = json.loads(candidate.read_text())
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        if payload.get("auth_mode") in {"chatgpt", "api_key"} or payload.get("tokens") or payload.get("api_key"):
            return True
    return False


def _load_docker_env_vars() -> dict[str, str]:
    try:
        output = subprocess.check_output(
            ["sudo", "docker", "inspect", "openclaw-starship", "--format", "{{json .Config.Env}}"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return {}
    try:
        env_list = json.loads(output)
    except Exception:
        return {}

    env_map: dict[str, str] = {}
    for item in env_list:
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        env_map[key] = value
    return env_map
