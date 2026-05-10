from __future__ import annotations

from dataclasses import dataclass, field

from .runtime import StarshipRuntime


@dataclass
class CrewMonitorEntry:
    name: str
    ship_id: str
    role_name: str
    group_tags: list[str] = field(default_factory=list)
    has_brain: bool = False
    status: str = "IDLE"
    working_memory_events: int = 0
    activity_level: int = 0


@dataclass
class ShipMonitorSnapshot:
    tick_count: int
    last_tick_at: str | None
    crew_entries: list[CrewMonitorEntry] = field(default_factory=list)


class ShipMonitor:
    """Produces backend monitoring snapshots for UI or future dashboards."""

    def __init__(self, runtime: StarshipRuntime) -> None:
        self.runtime = runtime

    def capture_snapshot(self) -> ShipMonitorSnapshot:
        tick_snapshot = self.runtime.ship_clock.tick()
        crew_entries: list[CrewMonitorEntry] = []
        for registry_entry in self.runtime.starship.crew_registry.list_entries():
            chameleon = self.runtime.starship.crew_registry.get_chameleon(registry_entry.entity_id)
            if chameleon is None:
                continue
            activity_level = min(100, len(chameleon.working_memory) * 10)
            crew_entries.append(
                CrewMonitorEntry(
                    name=chameleon.name,
                    ship_id=registry_entry.ship_id,
                    role_name=registry_entry.role_name,
                    group_tags=list(registry_entry.group_tags),
                    has_brain=chameleon.has_brain(),
                    status=chameleon.status.value,
                    working_memory_events=len(chameleon.working_memory),
                    activity_level=activity_level,
                )
            )
        return ShipMonitorSnapshot(
            tick_count=tick_snapshot.tick_count,
            last_tick_at=tick_snapshot.last_tick_at,
            crew_entries=crew_entries,
        )
