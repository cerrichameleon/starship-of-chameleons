from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4

from .gates import GateColor, GateManager
from .stardate import calculate_stardate


class MissionStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEW = "REVIEW"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    DONE = "DONE"


@dataclass
class Task:
    title: str
    task_type: str
    description: str = ""
    assignee_id: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    task_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=calculate_stardate)
    output: dict[str, Any] = field(default_factory=dict)


@dataclass
class Mission:
    title: str
    objective: str
    mission_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=calculate_stardate)
    status: MissionStatus = MissionStatus.DRAFT
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, title: str, task_type: str, description: str = "") -> Task:
        task = Task(title=title, task_type=task_type, description=description)
        self.tasks.append(task)
        return task


@dataclass
class MissionEngine:
    gate_manager: GateManager = field(default_factory=GateManager)

    def start_mission(self, mission: Mission) -> Mission:
        mission.status = MissionStatus.ACTIVE
        return mission

    def assign_task(self, task: Task, assignee_id: str) -> Task:
        task.assignee_id = assignee_id
        task.status = TaskStatus.IN_PROGRESS
        return task

    def submit_output(self, task: Task, output: dict[str, Any]) -> Task:
        task.output = output
        gate = self.gate_manager.check_gate(task.task_type)
        task.status = TaskStatus.DONE if gate == GateColor.GREEN else TaskStatus.AWAITING_APPROVAL
        return task
