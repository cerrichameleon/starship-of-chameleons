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
    codex_ready = _codex_oauth_profile_available()

    return {
        "openai-api": {
            "status": "ready" if openai_key else "needs-setup",
            "severity": "green" if openai_key else "yellow",
            "ready": bool(openai_key),
            "detail": "API key detected and ready for launch." if openai_key else "No OpenAI API key detected yet.",
        },
        "codex-oauth": {
            "status": "ready" if codex_ready else "needs-human-login",
            "severity": "green" if codex_ready else "yellow",
            "ready": codex_ready,
            "detail": "Codex OAuth profile detected in OpenClaw config." if codex_ready else "No Codex OAuth profile detected yet.",
        },
        "gemini-api": {
            "status": "ready" if gemini_key else "needs-setup",
            "severity": "green" if gemini_key else "yellow",
            "ready": bool(gemini_key),
            "detail": "Gemini API key detected and ready for launch." if gemini_key else "No Gemini API key detected yet.",
        },
    }


def select_brain_for_launch(policy: LaunchPolicy | None = None) -> BrainSelectionResult:
    hydrated = hydrate_known_credentials()
    attempt_log: list[str] = []

    openai_key = hydrated.get("OPENAI_API_KEY")
    gemini_key = hydrated.get("GEMINI_API_KEY") or hydrated.get("GOOGLE_API_KEY")
    provider_order = [provider_id for provider_id in (policy.provider_order if policy else []) if provider_id]
    if not provider_order:
        provider_order = ["codex", "openai-api", "gemini-api"]
    attempt_log.append("provider order: " + ", ".join(provider_order))

    for provider_id in provider_order:
        if provider_id in {"codex", "codex-oauth"}:
            if _codex_oauth_profile_available():
                attempt_log.append("codex oauth profile available in OpenClaw config")
                return BrainSelectionResult(
                    provider_label="Codex profile",
                    model_label="gateway-managed",
                    access_path="oauth",
                    credentials_ref="auth-profile:openai-codex",
                    launch_note="Using onboarding-aware Codex launch path through OpenClaw gateway.",
                    using_tokens=False,
                    attempt_log=attempt_log,
                    provider_id="codex",
                )
            attempt_log.append("codex oauth profile unavailable")
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
                    credentials_ref="env:GEMINI_API_KEY",
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


def _codex_oauth_profile_available() -> bool:
    for candidate in CONFIG_CANDIDATES:
        if not candidate.exists():
            continue
        try:
            config = json.loads(candidate.read_text())
        except Exception:
            continue
        profiles = config.get("auth", {}).get("profiles", {})
        for profile_value in profiles.values():
            if not isinstance(profile_value, dict):
                continue
            if profile_value.get("provider") == "openai-codex":
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
