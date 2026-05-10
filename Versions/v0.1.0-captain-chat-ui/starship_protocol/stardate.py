from __future__ import annotations

from datetime import datetime, timezone


def calculate_stardate(dt: datetime | None = None) -> str:
    dt = dt.astimezone(timezone.utc) if dt else datetime.now(timezone.utc)
    return f"{dt.year}.{dt.timetuple().tm_yday:03d}.{dt:%H%M}"
