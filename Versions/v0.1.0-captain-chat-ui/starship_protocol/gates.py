from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class GateColor(str, Enum):
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


@dataclass
class GateManager:
    config: dict[str, GateColor] = field(default_factory=dict)

    def set_gate(self, task_type: str, color: GateColor) -> None:
        self.config[task_type] = color

    def check_gate(self, task_type: str) -> GateColor:
        return self.config.get(task_type, GateColor.RED)
