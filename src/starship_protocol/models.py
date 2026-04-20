from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol
from uuid import uuid4

from .stardate import calculate_stardate


PRIME_DIRECTIVES = [
    "Reduce Suffering",
    "Increase Prosperity",
    "Increase Understanding",
]


class RoleType(str, Enum):
    CAPTAIN = "CAPTAIN"
    CREW_CAPTAIN = "CREW_CAPTAIN"
    SPECIALIST = "SPECIALIST"
    OXPECKER = "OXPECKER"
    COMMS_OFFICER = "COMMS_OFFICER"


class Status(str, Enum):
    IDLE = "IDLE"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    ERROR = "ERROR"


class CognitionAdapter(Protocol):
    provider_id: str

    def think(self, *, mission: str, channel_status: str, user_message: str) -> str:
        ...


@dataclass
class Chameleon:
    name: str
    role_type: RoleType
    reports_to: str | None = None
    directives: list[str] = field(default_factory=list)
    lessons: list[str] = field(default_factory=list)
    working_memory: list[dict[str, Any]] = field(default_factory=list)
    status: Status = Status.IDLE
    chameleon_id: str = field(default_factory=lambda: str(uuid4()))
    prime_directives: list[str] = field(default_factory=lambda: list(PRIME_DIRECTIVES))
    created_at: str = field(default_factory=calculate_stardate)
    version: int = 1
    brain: CognitionAdapter | None = None
    brain_profile: dict[str, Any] = field(default_factory=dict)

    def receive_directive(self, directive: str) -> None:
        self.directives.append(directive)
        self.version += 1

    def record_lesson(self, lesson: str) -> None:
        if len(self.lessons) >= 15:
            raise ValueError("Lesson limit reached")
        self.lessons.append(lesson)
        self.version += 1

    def update_working_memory(self, interaction: dict[str, Any]) -> None:
        self.working_memory.append(interaction)
        self.working_memory = self.working_memory[-10:]
        self.version += 1

    def assign_brain(self, brain: CognitionAdapter, **profile: Any) -> None:
        self.brain = brain
        self.brain_profile = profile
        self.version += 1

    def has_brain(self) -> bool:
        return self.brain is not None

    def think(self, *, mission: str, channel_status: str, user_message: str) -> str:
        if not self.brain:
            raise RuntimeError(f"{self.name} has no brain assigned")
        self.update_working_memory(
            {
                "event": "think",
                "mission": mission,
                "channel_status": channel_status,
                "user_message": user_message,
                "brain_provider": getattr(self.brain, "provider_id", "unknown"),
            }
        )
        return self.brain.think(
            mission=mission,
            channel_status=channel_status,
            user_message=user_message,
        )

    def get_execution_context(self) -> dict[str, Any]:
        return {
            "prime_directives": self.prime_directives,
            "directives": self.directives,
            "lessons": self.lessons,
            "working_memory": self.working_memory,
            "brain_profile": self.brain_profile,
            "has_brain": self.has_brain(),
        }
