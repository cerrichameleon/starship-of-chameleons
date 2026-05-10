from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib import request


@dataclass
class BrainConfig:
    model: str = "gpt-5.4"
    endpoint: str = "https://api.openai.com/v1/responses"
    credentials_ref: str = "oauth:openai-codex"
    provider_id: str = "openai-api"
    access_path: str = "api-key"
    gateway_url: str = "http://127.0.0.1:18789/v1/responses"
    gateway_token: str | None = None
    gateway_agent_id: str = "main"


class OpenAICodexBrain:
    """Generic live brain adapter for any Chameleon role."""

    provider_id: str = "openai-api"

    def __init__(
        self,
        config: BrainConfig | None = None,
        role_name: str = "Chameleon",
        mission_statement: str | None = None,
    ) -> None:
        self.config = config or BrainConfig()
        self.role_name = role_name
        self.provider_id = self.config.provider_id
        self.mission_statement = mission_statement or f"You are the {role_name} aboard the Starship."

    def think(self, *, mission: str, channel_status: str, user_message: str) -> str:
        if self.config.access_path == "oauth-gateway":
            return self._think_via_gateway(mission=mission, channel_status=channel_status, user_message=user_message)
        return self._think_via_direct_api(mission=mission, channel_status=channel_status, user_message=user_message)

    def _think_via_gateway(self, *, mission: str, channel_status: str, user_message: str) -> str:
        gateway_token = self.config.gateway_token or os.getenv("OPENCLAW_GATEWAY_TOKEN")
        if not gateway_token:
            return self._offline_reply(mission, channel_status, user_message, reason="missing OpenClaw gateway token")

        payload = {
            "model": "openclaw",
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                f"{self.mission_statement} "
                                "Stay concise, competent, and role-aware."
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
                                f"Status: {channel_status}\n"
                                f"Prompt: {user_message}"
                            ),
                        }
                    ],
                },
            ],
        }
        body = json.dumps(payload).encode("utf-8")
        req = request.Request(
            self.config.gateway_url,
            data=body,
            headers={
                "Authorization": f"Bearer {gateway_token}",
                "Content-Type": "application/json",
                "x-openclaw-agent-id": self.config.gateway_agent_id,
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
        return self._offline_reply(mission, channel_status, user_message, reason="empty gateway model response")

    def _think_via_direct_api(self, *, mission: str, channel_status: str, user_message: str) -> str:
        api_key = self._resolve_api_key()
        if not api_key:
            return self._offline_reply(mission, channel_status, user_message, reason="missing API credentials")

        payload = {
            "model": self.config.model,
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                f"{self.mission_statement} "
                                "Stay concise, competent, and role-aware."
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
                                f"Status: {channel_status}\n"
                                f"Prompt: {user_message}"
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

    def _resolve_api_key(self) -> str | None:
        if self.config.provider_id in {"codex", "openai-api", "openclaw"}:
            return os.getenv("OPENAI_API_KEY")
        if self.config.provider_id == "gemini-api":
            return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        return os.getenv("OPENAI_API_KEY")

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
            f"{self.role_name} (fallback): mission '{mission}' active, "
            f"status '{channel_status}', prompt '{user_message}', "
            f"live brain unavailable ({reason})."
        )
