from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class ShipTickSnapshot:
    tick_count: int
    last_tick_at: str | None


@dataclass
class ShipClock:
    tick_count: int = 0
    last_tick_at: str | None = None
    tick_history: list[str] = field(default_factory=list)

    def tick(self) -> ShipTickSnapshot:
        now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.tick_count += 1
        self.last_tick_at = now
        self.tick_history.append(now)
        self.tick_history = self.tick_history[-100:]
        return ShipTickSnapshot(tick_count=self.tick_count, last_tick_at=self.last_tick_at)

    def snapshot(self) -> ShipTickSnapshot:
        return ShipTickSnapshot(tick_count=self.tick_count, last_tick_at=self.last_tick_at)
