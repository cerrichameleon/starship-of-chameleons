from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .mission import Mission, MissionEngine
from .xwing_protocol import XWingStrikeCraft, build_default_xwing


@dataclass
class CaptainConversationTurn:
    role: str
    text: str


@dataclass
class CaptainConversationSession:
    craft: XWingStrikeCraft
    mission_engine: MissionEngine = field(default_factory=MissionEngine)
    history: list[CaptainConversationTurn] = field(default_factory=list)
    state_path: Path | None = None
    mission: Mission | None = None

    def __post_init__(self) -> None:
        if self.state_path:
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            self._load_state()

    def talk_to_captain(self, user_message: str) -> str:
        self.history.append(CaptainConversationTurn(role="user", text=user_message))

        if self.mission is None:
            self.mission = Mission(
                title="live captain conversation",
                objective="maintain a direct command conversation with the user",
            )
            self.mission_engine.start_mission(self.mission)

        if not self.craft.active_channel:
            try:
                self.craft.open_channel("captain-bridge")
            except Exception:
                pass

        reply = self.craft.captain_speak(user_message)
        self.history.append(CaptainConversationTurn(role="captain", text=reply))
        self._persist_state()
        return reply

    def summarize_state(self) -> dict[str, Any]:
        return {
            "ship": self.craft.name,
            "captain": self.craft.captain.name,
            "mission": self.mission.title if self.mission else None,
            "history_length": len(self.history),
            "channel_open": bool(self.craft.uhura.get_active_channel()),
            "captain_has_brain": self.craft.captain.has_brain(),
            "brain_profile": self.craft.captain.brain_profile,
        }

    def _persist_state(self) -> None:
        if not self.state_path:
            return
        payload = {
            "history": [{"role": turn.role, "text": turn.text} for turn in self.history],
            "mission": {
                "title": self.mission.title,
                "objective": self.mission.objective,
                "mission_id": self.mission.mission_id,
                "created_at": self.mission.created_at,
                "status": self.mission.status.value,
            }
            if self.mission
            else None,
        }
        self.state_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _load_state(self) -> None:
        if not self.state_path or not self.state_path.exists():
            return
        try:
            payload = json.loads(self.state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return
        self.history = [CaptainConversationTurn(**turn) for turn in payload.get("history", [])]
        mission_payload = payload.get("mission")
        if mission_payload:
            mission = Mission(
                title=mission_payload["title"],
                objective=mission_payload["objective"],
                mission_id=mission_payload["mission_id"],
                created_at=mission_payload["created_at"],
            )
            self.mission_engine.start_mission(mission)
            self.mission = mission


def build_captain_chat_session(base_path: Path | None = None, provider: str = "openclaw") -> CaptainConversationSession:
    root = base_path or Path.cwd()
    craft = build_default_xwing(root, provider=provider)
    state_path = root / "var" / "captain_chat_state.json"
    return CaptainConversationSession(craft=craft, state_path=state_path)
