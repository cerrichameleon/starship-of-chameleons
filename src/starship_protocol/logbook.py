from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .stardate import calculate_stardate


@dataclass
class LogEntry:
    entry_type: str
    content: str
    stardate: str = field(default_factory=calculate_stardate)
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class CaptainsLog:
    ship_name: str
    entries: list[LogEntry] = field(default_factory=list)

    def log(self, entry_type: str, content: str, **data: Any) -> LogEntry:
        entry = LogEntry(entry_type=entry_type, content=content, data=data)
        self.entries.append(entry)
        return entry

    def save(self, path: str | Path) -> None:
        payload = [asdict(entry) for entry in self.entries]
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
