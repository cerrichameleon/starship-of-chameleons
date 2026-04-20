from __future__ import annotations

import json
import secrets
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from .models import Chameleon, RoleType


STARDATE_FMT = "%Y-%m-%dT%H:%M:%SZ"


class ProtocolError(RuntimeError):
    """Base protocol error."""


class ChannelSecurityError(ProtocolError):
    """Raised when Uhura rejects an unsafe channel request."""


@dataclass
class SecureChannel:
    channel_id: str
    target: str
    opened_at: str
    expires_at: str
    transport: str = "local-bridge"
    state: str = "open"
    diagnostics: list[str] = field(default_factory=list)


@dataclass
class ChannelAuditRecord:
    timestamp: str
    event: str
    channel_id: str | None
    target: str
    notes: str


@dataclass
class Uhura(Chameleon):
    allowed_targets: set[str] = field(default_factory=set)
    audit_path: Path | None = None
    state_path: Path | None = None
    channel_ttl_seconds: int = 900
    _active_channels: dict[str, SecureChannel] = field(default_factory=dict, init=False, repr=False)

    def __init__(
        self,
        name: str,
        *,
        allowed_targets: set[str],
        audit_path: Path,
        state_path: Path,
        channel_ttl_seconds: int = 900,
        reports_to: str | None = None,
    ) -> None:
        super().__init__(name=name, role_type=RoleType.COMMS_OFFICER, reports_to=reports_to)
        self.allowed_targets = allowed_targets
        self.audit_path = audit_path
        self.state_path = state_path
        self.channel_ttl_seconds = channel_ttl_seconds
        self._active_channels = {}
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self._load_state()

    def open_channel(self, target: str) -> SecureChannel:
        existing = self.get_active_channel()
        if existing:
            raise ProtocolError("A channel is already open. Close it before opening another.")
        self._validate_target(target)
        now = datetime.now(UTC)
        channel = SecureChannel(
            channel_id=secrets.token_urlsafe(12),
            target=target,
            opened_at=now.strftime(STARDATE_FMT),
            expires_at=(now + timedelta(seconds=self.channel_ttl_seconds)).strftime(STARDATE_FMT),
            diagnostics=["tls-required", "captain-handoff-ready", "persistent-session-enabled"],
        )
        self._active_channels[channel.channel_id] = channel
        self.update_working_memory({"event": "channel_opened", "channel_id": channel.channel_id, "target": target})
        self._persist_state()
        self._audit("channel_opened", channel.channel_id, target, "Secure channel established.")
        return channel

    def notify_captain_channel_open(self, channel: SecureChannel) -> str:
        message = (
            f"Uhura: secure channel {channel.channel_id} to {channel.target} is open. "
            f"Transport={channel.transport}. Awaiting captain orders."
        )
        self.update_working_memory({"event": "captain_notified", "channel_id": channel.channel_id, "target": channel.target})
        self._audit("captain_notified", channel.channel_id, channel.target, message)
        return message

    def close_channel(self, channel_id: str, requested_by: str = "captain") -> SecureChannel:
        channel = self._require_channel(channel_id)
        channel.state = "closed"
        channel.diagnostics.append(f"closed-by:{requested_by}")
        self.update_working_memory({"event": "channel_closed", "channel_id": channel.channel_id, "target": channel.target})
        self._audit("channel_closed", channel.channel_id, channel.target, f"Closed by {requested_by}.")
        self._active_channels.pop(channel.channel_id, None)
        self._persist_state()
        return channel

    def diagnose_channel(self, channel_id: str) -> dict[str, Any]:
        channel = self._require_channel(channel_id)
        now = datetime.now(UTC)
        expires_at = datetime.strptime(channel.expires_at, STARDATE_FMT).replace(tzinfo=UTC)
        ttl_remaining = max(0, int((expires_at - now).total_seconds()))
        diagnosis = {
            "channel_id": channel.channel_id,
            "target": channel.target,
            "state": channel.state,
            "transport": channel.transport,
            "ttl_remaining_seconds": ttl_remaining,
            "diagnostics": list(channel.diagnostics),
        }
        self.update_working_memory({"event": "channel_diagnosed", "channel_id": channel.channel_id, "target": channel.target})
        self._audit("channel_diagnosed", channel.channel_id, channel.target, json.dumps(diagnosis))
        return diagnosis

    def get_active_channel(self) -> SecureChannel | None:
        self._expire_stale_channels()
        for channel in self._active_channels.values():
            if channel.state == "open":
                return channel
        return None

    def _validate_target(self, target: str) -> None:
        if target not in self.allowed_targets:
            self._audit("channel_denied", None, target, "Target not in allowlist.")
            raise ChannelSecurityError(f"Target '{target}' is not approved for Uhura routing.")

    def _require_channel(self, channel_id: str) -> SecureChannel:
        self._expire_stale_channels()
        channel = self._active_channels.get(channel_id)
        if not channel:
            raise ProtocolError(f"Unknown channel id: {channel_id}")
        return channel

    def _load_state(self) -> None:
        if not self.state_path or not self.state_path.exists():
            return
        try:
            payload = json.loads(self.state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            self._audit("state_corrupt", None, "local-state", "State file unreadable, ignoring.")
            return
        for entry in payload.get("active_channels", []):
            channel = SecureChannel(**entry)
            self._active_channels[channel.channel_id] = channel
        self._expire_stale_channels()

    def _persist_state(self) -> None:
        if not self.state_path:
            return
        payload = {
            "active_channels": [asdict(channel) for channel in self._active_channels.values() if channel.state == "open"]
        }
        self.state_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _expire_stale_channels(self) -> None:
        now = datetime.now(UTC)
        expired: list[str] = []
        for channel_id, channel in list(self._active_channels.items()):
            expires_at = datetime.strptime(channel.expires_at, STARDATE_FMT).replace(tzinfo=UTC)
            if expires_at <= now or channel.state != "open":
                expired.append(channel_id)
        for channel_id in expired:
            channel = self._active_channels.pop(channel_id)
            self._audit("channel_expired", channel.channel_id, channel.target, "Channel expired from persisted state.")
        if expired:
            self._persist_state()

    def _audit(self, event: str, channel_id: str | None, target: str, notes: str) -> None:
        if not self.audit_path:
            return
        record = ChannelAuditRecord(
            timestamp=datetime.now(UTC).strftime(STARDATE_FMT),
            event=event,
            channel_id=channel_id,
            target=target,
            notes=notes,
        )
        with self.audit_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record.__dict__) + "\n")
