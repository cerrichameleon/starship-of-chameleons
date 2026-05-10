from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class UsageRecord:
    actor_id: str
    actor_name: str
    provider_id: str
    estimated_input_tokens: int = 0
    estimated_output_tokens: int = 0
    estimated_cost_usd: float = 0.0
    event_count: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class UsageSnapshot:
    total_estimated_cost_usd: float
    totals_by_provider: dict[str, float]
    totals_by_actor: dict[str, float]
    records_by_actor: dict[str, UsageRecord]


class EstimatedUsageTracker:
    """Tracks approximate per-Chameleon and per-provider usage for local transparency."""

    def __init__(self) -> None:
        self._records_by_actor: dict[str, UsageRecord] = {}

    def record_usage(
        self,
        *,
        actor_id: str,
        actor_name: str,
        provider_id: str,
        estimated_input_tokens: int,
        estimated_output_tokens: int,
        estimated_cost_usd: float,
        metadata: dict[str, Any] | None = None,
    ) -> UsageRecord:
        record = self._records_by_actor.get(actor_id)
        if record is None:
            record = UsageRecord(actor_id=actor_id, actor_name=actor_name, provider_id=provider_id)
            self._records_by_actor[actor_id] = record
        record.estimated_input_tokens += estimated_input_tokens
        record.estimated_output_tokens += estimated_output_tokens
        record.estimated_cost_usd += estimated_cost_usd
        record.event_count += 1
        record.metadata.update(metadata or {})
        return record

    def snapshot(self) -> UsageSnapshot:
        total_estimated_cost_usd = sum(record.estimated_cost_usd for record in self._records_by_actor.values())
        totals_by_provider: dict[str, float] = {}
        totals_by_actor: dict[str, float] = {}
        for actor_id, record in self._records_by_actor.items():
            totals_by_actor[actor_id] = record.estimated_cost_usd
            totals_by_provider[record.provider_id] = totals_by_provider.get(record.provider_id, 0.0) + record.estimated_cost_usd
        return UsageSnapshot(
            total_estimated_cost_usd=total_estimated_cost_usd,
            totals_by_provider=totals_by_provider,
            totals_by_actor=totals_by_actor,
            records_by_actor=dict(self._records_by_actor),
        )
