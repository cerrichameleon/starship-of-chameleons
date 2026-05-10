from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from .brains import BrainConfig, OpenAICodexBrain

CAPTAIN_IDENTITY_PATH = Path(__file__).with_name("CAPTAIN_IDENTITY.md")


DIRECT_API_ENDPOINTS = {
    "openai-api": "https://api.openai.com/v1/responses",
    "gemini-api": "https://generativelanguage.googleapis.com/v1beta/openai/responses",
}


OPENCLAW_CONFIG_CANDIDATES = [
    Path.home() / ".openclaw" / "openclaw.json",
    Path("/home/node/.openclaw/openclaw.json"),
]


@dataclass
class AgentSpec:
    role_name: str
    provider_id: str
    model_id: str
    credentials_ref: str
    capabilities: list[str] = field(default_factory=list)


@dataclass
class BrainSelectionResult:
    provider_label: str
    model_label: str
    access_path: str
    credentials_ref: str
    launch_note: str
    using_tokens: bool
    attempt_log: list[str] = field(default_factory=list)
    provider_id: str = "unknown"


class CaptainBrain(Protocol):
    def think(self, *, mission: str, channel_status: str, user_message: str) -> str:
        ...


class AgentProvider(Protocol):
    provider_id: str

    def create_agent(self, spec: AgentSpec) -> dict:
        ...

    def create_captain_brain(self, spec: AgentSpec) -> CaptainBrain:
        ...


@dataclass
class NullCaptainBrain:
    provider_id: str

    def think(self, *, mission: str, channel_status: str, user_message: str) -> str:
        return (
            f"Captain ({self.provider_id} placeholder): mission '{mission}' active, "
            f"status '{channel_status}', order '{user_message}'."
        )


@dataclass
class OpenClawProvider:
    provider_id: str = "openai-api"

    def create_agent(self, spec: AgentSpec) -> dict:
        return {
            "provider": self.provider_id,
            "role_name": spec.role_name,
            "model_id": spec.model_id,
            "credentials_ref": spec.credentials_ref,
            "capabilities": spec.capabilities,
            "status": "embodied",
        }

    def create_captain_brain(self, spec: AgentSpec) -> CaptainBrain:
        identity_text = _load_captain_identity_text()
        mission_statement = (
            f"{identity_text}\n\n"
            "You are role-aware, practical, concise, and honest about what is and is not implemented. "
            "You follow the Prime Directives: Reduce Suffering, Increase Prosperity, Increase Understanding. "
            "When doing software work, prefer readable names, clear structure, explicit reasoning, good documentation, and honest status updates. "
            f"Your active capabilities are: {', '.join(spec.capabilities) if spec.capabilities else 'general problem solving'}."
        )
        access_path = "oauth-gateway" if spec.credentials_ref.startswith("auth-profile:") else "api-key"
        endpoint = DIRECT_API_ENDPOINTS.get(spec.provider_id, "https://api.openai.com/v1/responses")
        return OpenAICodexBrain(
            BrainConfig(
                model=spec.model_id,
                endpoint=endpoint,
                credentials_ref=spec.credentials_ref,
                provider_id=spec.provider_id,
                access_path=access_path,
                gateway_token=_load_gateway_token(),
            ),
            role_name=spec.role_name,
            mission_statement=mission_statement,
        )


@dataclass
class MockProvider:
    provider_id: str = "mock"
    canned_responses: list[str] | None = None

    def create_agent(self, spec: AgentSpec) -> dict[str, Any]:
        return {
            "provider": self.provider_id,
            "role_name": spec.role_name,
            "model_id": spec.model_id,
            "credentials_ref": spec.credentials_ref,
            "capabilities": spec.capabilities,
            "status": "simulated",
        }

    def create_captain_brain(self, spec: AgentSpec) -> CaptainBrain:
        return NullCaptainBrain(provider_id=self.provider_id)


def _load_captain_identity_text() -> str:
    identity_parts: list[str] = []
    try:
        identity_parts.append(CAPTAIN_IDENTITY_PATH.read_text().strip())
    except Exception:
        identity_parts.append(
            "You are the Captain of the Starship of Chameleons. The starship is the crew. "
            "Your job is to lead a mission-specific group of AI chameleons, shape the right crew for the task, delegate clearly, and report honestly about what is and is not implemented."
        )

    whitepaper_path = Path(__file__).resolve().parents[2] / "docs" / "Chameleon_Starship_Protocol_v2.0.0_WHITEPAPER.md"
    try:
        whitepaper_text = whitepaper_path.read_text().strip()
    except Exception:
        whitepaper_text = ""
    if whitepaper_text:
        identity_parts.append(
            "The following white paper is background doctrine for the Starship of Chameleons. Use it to understand the intended system, crew model, memory model, and mission structure. Be honest about which parts are implemented now and which parts are still aspirational.\n\n"
            + whitepaper_text
        )
    return "\n\n".join(identity_parts)


def _load_gateway_token() -> str | None:
    for candidate in OPENCLAW_CONFIG_CANDIDATES:
        if not candidate.exists():
            continue
        try:
            config = json.loads(candidate.read_text())
        except Exception:
            continue
        token = config.get("gateway", {}).get("auth", {}).get("token")
        if token:
            return str(token)
    return None
