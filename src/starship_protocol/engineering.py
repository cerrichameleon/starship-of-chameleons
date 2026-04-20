from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .models import Chameleon, CognitionAdapter, RoleType
from .providers import AgentProvider, AgentSpec


class EngineeringMode(str, Enum):
    FRUGAL = "FRUGAL"
    BALANCED = "BALANCED"
    HIGH_ACCURACY = "HIGH_ACCURACY"
    NIGHT_SHIFT = "NIGHT_SHIFT"
    CRITICAL_MISSION = "CRITICAL_MISSION"


@dataclass
class ModelCandidate:
    name: str
    strength: int
    cost_tier: int
    tags: set[str] = field(default_factory=set)


@dataclass
class ChiefEngineer(Chameleon):
    mode: EngineeringMode = EngineeringMode.BALANCED
    available_models: list[ModelCandidate] = field(default_factory=list)

    def __init__(self, name: str, reports_to: str | None = None):
        super().__init__(name=name, role_type=RoleType.SPECIALIST, reports_to=reports_to)
        self.mode = EngineeringMode.BALANCED
        self.available_models = []

    def register_model(self, name: str, strength: int, cost_tier: int, tags: set[str] | None = None) -> None:
        self.available_models.append(
            ModelCandidate(name=name, strength=strength, cost_tier=cost_tier, tags=tags or set())
        )

    def choose_model(self, task_type: str, complexity: int = 1, needs_vision: bool = False) -> dict[str, Any]:
        candidates = self.available_models[:]
        if needs_vision:
            candidates = [c for c in candidates if "vision" in c.tags]

        if not candidates:
            return {
                "mode": self.mode.value,
                "task_type": task_type,
                "decision": "no_registered_models",
            }

        min_strength = self._required_strength(complexity)
        viable = [c for c in candidates if c.strength >= min_strength]
        if not viable:
            viable = sorted(candidates, key=lambda c: (-c.strength, c.cost_tier))[:1]

        chosen = sorted(viable, key=lambda c: (self._cost_weight(c.cost_tier), c.strength))[0]
        return {
            "mode": self.mode.value,
            "task_type": task_type,
            "complexity": complexity,
            "needs_vision": needs_vision,
            "chosen_model": chosen.name,
            "chosen_strength": chosen.strength,
            "chosen_cost_tier": chosen.cost_tier,
        }

    def outfit_chameleon(self, chameleon: Chameleon, brain: CognitionAdapter, **profile: Any) -> None:
        chameleon.assign_brain(brain, outfitted_by=self.name, engineering_mode=self.mode.value, **profile)

    def outfit_with_provider(
        self,
        chameleon: Chameleon,
        provider: AgentProvider,
        *,
        model_id: str,
        credentials_ref: str,
        capabilities: list[str] | None = None,
    ) -> None:
        spec = AgentSpec(
            role_name=chameleon.role_type.value,
            provider_id=provider.provider_id,
            model_id=model_id,
            credentials_ref=credentials_ref,
            capabilities=capabilities or [],
        )
        brain = provider.create_captain_brain(spec)
        self.outfit_chameleon(
            chameleon,
            brain,
            provider_id=provider.provider_id,
            model_id=model_id,
            credentials_ref=credentials_ref,
            capabilities=spec.capabilities,
        )

    def _required_strength(self, complexity: int) -> int:
        if self.mode == EngineeringMode.CRITICAL_MISSION:
            return max(4, complexity + 1)
        if self.mode == EngineeringMode.HIGH_ACCURACY:
            return max(3, complexity)
        if self.mode == EngineeringMode.FRUGAL:
            return max(1, complexity - 1)
        if self.mode == EngineeringMode.NIGHT_SHIFT:
            return max(1, complexity - 1)
        return max(2, complexity)

    def _cost_weight(self, cost_tier: int) -> int:
        if self.mode == EngineeringMode.CRITICAL_MISSION:
            return cost_tier + 3
        if self.mode == EngineeringMode.HIGH_ACCURACY:
            return cost_tier + 2
        if self.mode == EngineeringMode.BALANCED:
            return cost_tier
        if self.mode == EngineeringMode.NIGHT_SHIFT:
            return max(0, cost_tier - 1)
        return max(0, cost_tier - 2)
