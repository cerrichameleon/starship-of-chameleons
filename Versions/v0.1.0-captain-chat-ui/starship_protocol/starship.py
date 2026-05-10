from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .engineering import ChiefEngineer
from .mission import Mission, MissionEngine, Task
from .registry import CrewRegistry, CrewRegistryEntry
from .roles import Captain, Specialist


@dataclass
class Starship:
    name: str
    ship_class: str
    captain: Captain
    chief_engineer: ChiefEngineer | None = None
    crew: list[Specialist] = field(default_factory=list)
    mission_engine: MissionEngine = field(default_factory=MissionEngine)
    crew_registry: CrewRegistry = field(default_factory=CrewRegistry)

    def __post_init__(self) -> None:
        self.crew_registry.register(
            self.captain,
            role_name="captain",
            ship_id_prefix="captain",
            group_tags=["command"],
            reports_to=None,
        )
        if self.chief_engineer is not None:
            self.crew_registry.register(
                self.chief_engineer,
                role_name="chief-engineer",
                ship_id_prefix="chief-engineer",
                group_tags=["engineering", "command"],
                reports_to=self.captain.chameleon_id,
            )

    def register_crew(
        self,
        chameleon: Specialist,
        *,
        role_name: str | None = None,
        ship_id_prefix: str | None = None,
        group_tags: list[str] | None = None,
    ) -> CrewRegistryEntry:
        self.crew.append(chameleon)
        normalized_role_name = role_name or chameleon.focus_area or "specialist"
        normalized_prefix = ship_id_prefix or normalized_role_name.replace(" ", "-")
        normalized_groups = group_tags or [chameleon.focus_area]
        return self.crew_registry.register(
            chameleon,
            role_name=normalized_role_name,
            ship_id_prefix=normalized_prefix,
            group_tags=normalized_groups,
            reports_to=chameleon.reports_to,
        )

    def find_specialist(self, focus_area: str) -> Specialist | None:
        for crew_member in self.crew:
            if crew_member.focus_area == focus_area:
                return crew_member
        return None

    def delegate(self, *, focus_area: str, title: str, description: str) -> dict[str, Any]:
        specialist = self.find_specialist(focus_area)
        if not specialist:
            return {
                "status": "no_specialist_available",
                "focus_area": focus_area,
                "title": title,
            }

        mission = Mission(title=f"delegation:{title}", objective=description)
        self.mission_engine.start_mission(mission)
        task = mission.add_task(title=title, task_type=focus_area, description=description)
        self.mission_engine.assign_task(task, specialist.chameleon_id)

        specialist_reply = specialist.think(
            mission=mission.objective,
            channel_status=f"delegated by Captain {self.captain.name}",
            user_message=description,
        )
        task.output = {"reply": specialist_reply}

        return {
            "status": "delegated",
            "mission_id": mission.mission_id,
            "task_id": task.task_id,
            "specialist": specialist.name,
            "focus_area": specialist.focus_area,
            "reply": specialist_reply,
        }
