from __future__ import annotations

from dataclasses import dataclass, field

from .mission import Mission, Task
from .models import Chameleon, RoleType


@dataclass
class Specialist(Chameleon):
    focus_area: str = "general"
    skill_ids: list[str] = field(default_factory=list)
    peer_review_queue: list[dict] = field(default_factory=list)

    def __init__(self, name: str, focus_area: str = "general", reports_to: str | None = None):
        super().__init__(name=name, role_type=RoleType.SPECIALIST, reports_to=reports_to)
        self.focus_area = focus_area
        self.skill_ids = []
        self.peer_review_queue = []

    def execute_task(self, task: Task, context: dict | None = None) -> dict:
        return {
            "task_id": task.task_id,
            "specialist": self.name,
            "focus_area": self.focus_area,
            "status": "completed",
            "context": context or {},
        }

    def submit_for_peer_review(self, output: dict) -> str:
        self.peer_review_queue.append(output)
        return "queued"


@dataclass
class Oxpecker(Specialist):
    assigned_entity_id: str | None = None

    def __init__(self, name: str, assigned_entity_id: str | None = None, reports_to: str | None = None):
        super().__init__(name=name, focus_area="quality_control", reports_to=reports_to)
        self.role_type = RoleType.OXPECKER
        self.assigned_entity_id = assigned_entity_id

    def review_output(self, output: dict) -> dict:
        return {
            "reviewer": self.name,
            "assigned_entity_id": self.assigned_entity_id,
            "approved": True,
            "notes": "Initial Oxpecker pass complete.",
            "output": output,
        }


@dataclass
class CrewCaptain(Chameleon):
    managed_entities: list[str] = field(default_factory=list)

    def __init__(self, name: str, reports_to: str | None = None):
        super().__init__(name=name, role_type=RoleType.CREW_CAPTAIN, reports_to=reports_to)
        self.managed_entities = []

    def add_specialist(self, specialist: Specialist) -> None:
        self.managed_entities.append(specialist.chameleon_id)

    def assign_task(self, task: Task, specialist: Specialist) -> Task:
        task.assignee_id = specialist.chameleon_id
        return task


@dataclass
class Captain(Chameleon):
    managed_entities: list[str] = field(default_factory=list)

    def __init__(self, name: str):
        super().__init__(name=name, role_type=RoleType.CAPTAIN, reports_to=None)
        self.managed_entities = []

    def add_crew_captain(self, crew_captain: CrewCaptain) -> None:
        self.managed_entities.append(crew_captain.chameleon_id)

    def decompose_mission(self, mission: Mission) -> list[Task]:
        return mission.tasks
