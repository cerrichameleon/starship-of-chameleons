from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass
class ActivityLogEntry:
    timestamp: str
    actor_id: str
    actor_name: str
    event_type: str
    message: str
    metadata: dict[str, Any]


class ActivityLogStore:
    """Writes per-Chameleon activity logs to disk inside the active project workspace."""

    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path
        self.root_path.mkdir(parents=True, exist_ok=True)

    def append_entry(
        self,
        *,
        actor_id: str,
        actor_name: str,
        event_type: str,
        message: str,
        metadata: dict[str, Any] | None = None,
    ) -> ActivityLogEntry:
        entry = ActivityLogEntry(
            timestamp=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            actor_id=actor_id,
            actor_name=actor_name,
            event_type=event_type,
            message=message,
            metadata=metadata or {},
        )
        path = self.root_path / f"{actor_id}.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry.__dict__) + "\n")
        return entry

    def read_recent_entries(self, actor_id: str, limit: int = 20) -> list[ActivityLogEntry]:
        path = self.root_path / f"{actor_id}.jsonl"
        if not path.exists():
            return []
        lines = path.read_text(encoding="utf-8").splitlines()[-limit:]
        return [ActivityLogEntry(**json.loads(line)) for line in lines if line.strip()]
