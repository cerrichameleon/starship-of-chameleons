from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass
class WorkSessionSnapshot:
    started_at: str
    last_updated_at: str
    elapsed_seconds: int


class WorkTracker:
    """Tracks elapsed project work time for the current runtime session."""

    def __init__(self) -> None:
        started_at = datetime.now(UTC)
        self._started_at = started_at
        self._last_updated_at = started_at

    def touch(self) -> WorkSessionSnapshot:
        self._last_updated_at = datetime.now(UTC)
        return self.snapshot()

    def snapshot(self) -> WorkSessionSnapshot:
        elapsed_seconds = int((self._last_updated_at - self._started_at).total_seconds())
        return WorkSessionSnapshot(
            started_at=self._started_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            last_updated_at=self._last_updated_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            elapsed_seconds=elapsed_seconds,
        )
