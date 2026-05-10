from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable
from uuid import uuid4

from .models import Chameleon


@dataclass
class CrewRegistryEntry:
    entity_id: str
    ship_id: str
    role_name: str
    group_tags: list[str] = field(default_factory=list)
    reports_to: str | None = None
    duty_status: str = "active"


class CrewRegistry:
    """Ship-owned registry for human-legible and machine-stable crew identity."""

    def __init__(self) -> None:
        self._entries_by_entity_id: dict[str, CrewRegistryEntry] = {}
        self._crew_by_entity_id: dict[str, Chameleon] = {}
        self._sequence_by_prefix: dict[str, int] = {}

    def register(
        self,
        chameleon: Chameleon,
        *,
        role_name: str,
        ship_id_prefix: str,
        group_tags: Iterable[str] | None = None,
        reports_to: str | None = None,
    ) -> CrewRegistryEntry:
        entity_id = getattr(chameleon, "entity_id", None) or str(uuid4())
        setattr(chameleon, "entity_id", entity_id)

        if entity_id in self._entries_by_entity_id:
            return self._entries_by_entity_id[entity_id]

        sequence_number = self._sequence_by_prefix.get(ship_id_prefix, 0) + 1
        self._sequence_by_prefix[ship_id_prefix] = sequence_number
        ship_id = f"{ship_id_prefix}-{sequence_number:03d}"
        entry = CrewRegistryEntry(
            entity_id=entity_id,
            ship_id=ship_id,
            role_name=role_name,
            group_tags=list(group_tags or []),
            reports_to=reports_to,
        )
        self._entries_by_entity_id[entity_id] = entry
        self._crew_by_entity_id[entity_id] = chameleon
        setattr(chameleon, "ship_id", ship_id)
        return entry

    def get_entry(self, entity_id: str) -> CrewRegistryEntry | None:
        return self._entries_by_entity_id.get(entity_id)

    def get_chameleon(self, entity_id: str) -> Chameleon | None:
        return self._crew_by_entity_id.get(entity_id)

    def list_entries(self) -> list[CrewRegistryEntry]:
        return list(self._entries_by_entity_id.values())

    def find_by_group(self, group_tag: str) -> list[CrewRegistryEntry]:
        return [entry for entry in self._entries_by_entity_id.values() if group_tag in entry.group_tags]
