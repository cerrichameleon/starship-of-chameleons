from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .runtime import StarshipRuntime


@dataclass
class CaptainCrewProposal:
    mission_prompt: str
    rationale: str
    proposed_roles: list[dict[str, Any]] = field(default_factory=list)
    research_notes: list[str] = field(default_factory=list)
    approval_status: str = "draft"


class CaptainConsole:
    """Interface-independent Captain-facing application service."""

    def __init__(self, runtime: StarshipRuntime) -> None:
        self.runtime = runtime

    def submit_chat_message(self, message_text: str) -> str:
        return self.runtime.captain_chat_session.talk_to_captain(message_text)

    def summarize_chat_history(self) -> list[dict[str, str]]:
        return [
            {"role": turn.role, "text": turn.text}
            for turn in self.runtime.captain_chat_session.history
        ]

    def draft_crew_proposal(self, mission_prompt: str) -> CaptainCrewProposal:
        captain_reply = self.runtime.starship.captain.think(
            mission="design an appropriate crew structure for a new mission",
            channel_status="captain's console planning mode",
            user_message=(
                "Analyze the following mission request, infer a suitable initial crew structure, and explain your reasoning. "
                "Do not instantiate crew yet. Produce a concise rationale plus a role list.\n\n"
                f"Mission request: {mission_prompt}"
            ),
        )
        return CaptainCrewProposal(
            mission_prompt=mission_prompt,
            rationale=captain_reply,
            proposed_roles=[],
            research_notes=[],
            approval_status="draft",
        )
