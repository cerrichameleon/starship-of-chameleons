from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import request

from .comms import ProtocolError, SecureChannel, Uhura
from .providers import AgentSpec, MockProvider, OpenClawProvider
from .roles import Captain


@dataclass
class CaptainBrainConfig:
    model: str = "gpt-5.4"
    endpoint: str = "https://api.openai.com/v1/responses"
    credentials_ref: str = "oauth:openai-codex"


class OpenAICodexCaptainBrain:
    """Minimal Captain brain using OpenAI Responses API compatible auth."""

    def __init__(self, config: CaptainBrainConfig | None = None) -> None:
        self.config = config or CaptainBrainConfig()

    def think(self, *, mission: str, channel_status: str, user_message: str) -> str:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return self._offline_reply(mission, channel_status, user_message, reason="missing OPENAI_API_KEY")

        payload = {
            "model": self.config.model,
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "You are the Captain of a light strike craft. "
                                "Uhura handles secure channel establishment and teardown. "
                                "Respond with concise bridge commands and status."
                            ),
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                f"Mission: {mission}\n"
                                f"Uhura status: {channel_status}\n"
                                f"Captain prompt: {user_message}"
                            ),
                        }
                    ],
                },
            ],
        }
        body = json.dumps(payload).encode("utf-8")
        req = request.Request(
            self.config.endpoint,
            data=body,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # pragma: no cover - network dependent
            return self._offline_reply(mission, channel_status, user_message, reason=str(exc))

        text = self._extract_text(data)
        if text:
            return text
        return self._offline_reply(mission, channel_status, user_message, reason="empty model response")

    def _extract_text(self, data: dict[str, Any]) -> str:
        output = data.get("output", [])
        parts: list[str] = []
        for item in output:
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"}:
                    text = content.get("text")
                    if text:
                        parts.append(text)
        return "\n".join(parts).strip()

    def _offline_reply(self, mission: str, channel_status: str, user_message: str, *, reason: str) -> str:
        return (
            "Captain (fallback): mission remains active. "
            f"Uhura reports {channel_status}. "
            f"Latest order interpreted as: '{user_message}'. "
            f"Codex link unavailable ({reason})."
        )


@dataclass
class XWingStrikeCraft:
    name: str
    captain: Captain
    uhura: Uhura
    mission: str
    active_channel: SecureChannel | None = None

    def __post_init__(self) -> None:
        self.active_channel = self.uhura.get_active_channel()

    def open_channel(self, target: str) -> str:
        active = self.uhura.get_active_channel()
        if active and active.state == "open":
            self.active_channel = active
            raise ProtocolError("A channel is already open. Close it before opening another.")
        self.active_channel = self.uhura.open_channel(target)
        self.captain.update_working_memory({"event": "uhura_channel_ready", "channel_id": self.active_channel.channel_id})
        return self.uhura.notify_captain_channel_open(self.active_channel)

    def captain_speak(self, prompt: str) -> str:
        self.active_channel = self.uhura.get_active_channel()
        channel_status = (
            f"channel {self.active_channel.channel_id} open to {self.active_channel.target}"
            if self.active_channel
            else "no active channel"
        )
        self.captain.update_working_memory({"event": "captain_prompt", "prompt": prompt, "channel_status": channel_status})
        return self.captain.think(
            mission=self.mission,
            channel_status=channel_status,
            user_message=prompt,
        )

    def diagnose_channel(self) -> dict[str, Any]:
        self.active_channel = self.uhura.get_active_channel()
        if not self.active_channel:
            raise ProtocolError("No active channel to diagnose.")
        return self.uhura.diagnose_channel(self.active_channel.channel_id)

    def close_channel(self) -> str:
        self.active_channel = self.uhura.get_active_channel()
        if not self.active_channel:
            raise ProtocolError("No active channel to close.")
        closed = self.uhura.close_channel(self.active_channel.channel_id)
        self.captain.update_working_memory({"event": "channel_closed", "channel_id": closed.channel_id})
        self.active_channel = None
        return f"Uhura: secure channel {closed.channel_id} to {closed.target} is now closed."


def build_default_xwing(base_path: Path | None = None, provider: str = "openclaw") -> XWingStrikeCraft:
    root = base_path or Path.cwd()
    audit_path = root / "var" / "uhura_audit.log"
    state_path = root / "var" / "uhura_state.json"
    provider_registry = {
        "openclaw": OpenClawProvider(),
        "mock": MockProvider(),
    }
    provider_impl = provider_registry[provider]
    spec = AgentSpec(
        role_name="Captain",
        provider_id=provider,
        model_id=os.getenv("STARSHIP_CAPTAIN_MODEL", "gpt-5.4"),
        credentials_ref="auth-profile:openai-codex:mattcleere@gmail.com",
        capabilities=["command", "planning", "bridge-comms"],
    )
    brain = provider_impl.create_captain_brain(spec)
    captain = Captain(name="Captain Kirk Skywalker")
    captain.assign_brain(
        brain,
        provider_id=provider,
        model_id=spec.model_id,
        credentials_ref=spec.credentials_ref,
        capabilities=spec.capabilities,
    )
    uhura = Uhura(
        name="Uhura-D2",
        allowed_targets={"captain-bridge", "mission-control", "user-dm"},
        audit_path=audit_path,
        state_path=state_path,
        reports_to=captain.chameleon_id,
    )
    return XWingStrikeCraft(
        name="Red Five / Enterprise Hybrid",
        captain=captain,
        uhura=uhura,
        mission="Maintain command authority while keeping communications compartmentalized.",
    )
