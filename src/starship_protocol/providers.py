from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class AgentSpec:
    role_name: str
    provider_id: str
    model_id: str
    credentials_ref: str
    capabilities: list[str] = field(default_factory=list)


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
    provider_id: str = "openclaw"

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
        from .xwing_protocol import CaptainBrainConfig, OpenAICodexCaptainBrain

        return OpenAICodexCaptainBrain(
            CaptainBrainConfig(
                model=spec.model_id,
                credentials_ref=spec.credentials_ref,
            )
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
