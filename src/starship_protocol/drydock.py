from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .runtime import StarshipRuntime


@dataclass
class DryDockStatus:
    ship_name: str
    readiness: str
    mission_preparation_note: str
    current_focus: str
    checklist: list[str] = field(default_factory=list)


class DryDockController:
    """Represents the Starship being alive, docked, and preparing for launch."""

    def __init__(self, runtime: StarshipRuntime) -> None:
        self.runtime = runtime
        self.status = DryDockStatus(
            ship_name=runtime.starship.name,
            readiness="dry-dock",
            mission_preparation_note="Preparing the first mission: build the Starship program itself.",
            current_focus="stabilize runtime, monitor crew, and prepare launch controls",
            checklist=[
                "Captain online",
                "Chief Engineer online",
                "Uhura online",
                "crew registry active",
                "internal communications available",
                "monitoring and logging being wired in",
            ],
        )

    def snapshot(self) -> DryDockStatus:
        return self.status

    def is_in_drydock(self) -> bool:
        return self.status.readiness == "dry-dock"
