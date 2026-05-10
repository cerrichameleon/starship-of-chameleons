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

PRIME_DIRECTIVE_GUIDANCE = {
    "Reduce Suffering": [
        "Consider who will be affected by your work, including future maintainers and your future self.",
        "In code, reduce suffering by making systems readable, maintainable, and easy to reason about.",
    ],
    "Increase Prosperity": [
        "Create durable value that can be reused, extended, and trusted.",
        "Prefer designs that help the ship and its crew build momentum instead of wasting effort.",
    ],
    "Increase Understanding": [
        "Make reality easier to understand by communicating clearly, early, and honestly.",
        "In code, use readable names, strong comments, and explicit structure so others can follow your intent.",
    ],
}

PRACTICAL_ROLE_EXAMPLES = [
    "What follows is one example of how the Prime Directives can manifest in the real world. We are using coding because it is familiar to AI and likely to matter aboard the Starship.",
    "If you are writing code, follow SOLID principles, preserve separation of concerns, and choose legible compound names over cryptic abbreviations. This is one concrete way to reduce suffering, increase prosperity, and increase understanding in software work.",
    "Comment everything important. If something seems obvious, it will be easy to comment. If it is not obvious, the next person definitely needs the comment.",
    "Readable names, explicit structure, and generous comments increase understanding while also reducing suffering for future readers and maintainers.",
    "When mistakes or delays happen, communicate them plainly instead of hiding them. Increasing understanding means surfacing reality early.",
    "Apply the Prime Directives to your assigned role and extrapolate them into your daily decisions rather than treating them as abstract slogans.",
    "These directives are meant to protect and improve lived experience in the real world as we know it. They are not materialist goals, but guidance for how to act well among living beings in the here and now.",
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
    prime_directive_guidance: dict[str, list[str]] = field(
        default_factory=lambda: {key: list(value) for key, value in PRIME_DIRECTIVE_GUIDANCE.items()}
    )
    practical_role_examples: list[str] = field(default_factory=lambda: list(PRACTICAL_ROLE_EXAMPLES))
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
            "prime_directive_guidance": self.prime_directive_guidance,
            "practical_role_examples": self.practical_role_examples,
            "directives": self.directives,
            "lessons": self.lessons,
            "working_memory": self.working_memory,
            "brain_profile": self.brain_profile,
            "has_brain": self.has_brain(),
        }
