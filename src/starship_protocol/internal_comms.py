from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4


class CommunicationMode(str, Enum):
    DIRECT = "DIRECT"
    MAILBOX = "MAILBOX"
    BLACKBOARD = "BLACKBOARD"


@dataclass
class InternalMessage:
    message_id: str
    mode: CommunicationMode
    sender_id: str
    recipient_id: str | None
    group_tag: str | None
    subject: str
    content: str
    mission_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class BlackboardEntry:
    entry_id: str
    author_id: str
    board_name: str
    content: str
    mission_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class InternalCommunicationsHub:
    """Provides direct, mailbox, and blackboard collaboration modes inside a Starship."""

    def __init__(self) -> None:
        self._direct_messages: list[InternalMessage] = []
        self._mailboxes: dict[str, list[InternalMessage]] = {}
        self._blackboards: dict[str, list[BlackboardEntry]] = {}

    def send_direct_message(
        self,
        *,
        sender_id: str,
        recipient_id: str,
        subject: str,
        content: str,
        mission_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> InternalMessage:
        message = InternalMessage(
            message_id=str(uuid4()),
            mode=CommunicationMode.DIRECT,
            sender_id=sender_id,
            recipient_id=recipient_id,
            group_tag=None,
            subject=subject,
            content=content,
            mission_id=mission_id,
            metadata=metadata or {},
        )
        self._direct_messages.append(message)
        return message

    def queue_mailbox_message(
        self,
        *,
        sender_id: str,
        recipient_id: str,
        subject: str,
        content: str,
        mission_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> InternalMessage:
        message = InternalMessage(
            message_id=str(uuid4()),
            mode=CommunicationMode.MAILBOX,
            sender_id=sender_id,
            recipient_id=recipient_id,
            group_tag=None,
            subject=subject,
            content=content,
            mission_id=mission_id,
            metadata=metadata or {},
        )
        self._mailboxes.setdefault(recipient_id, []).append(message)
        return message

    def read_mailbox(self, recipient_id: str) -> list[InternalMessage]:
        return list(self._mailboxes.get(recipient_id, []))

    def post_blackboard_entry(
        self,
        *,
        author_id: str,
        board_name: str,
        content: str,
        mission_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> BlackboardEntry:
        entry = BlackboardEntry(
            entry_id=str(uuid4()),
            author_id=author_id,
            board_name=board_name,
            content=content,
            mission_id=mission_id,
            metadata=metadata or {},
        )
        self._blackboards.setdefault(board_name, []).append(entry)
        return entry

    def read_blackboard(self, board_name: str) -> list[BlackboardEntry]:
        return list(self._blackboards.get(board_name, []))

    def get_direct_messages_for_participant(self, participant_id: str) -> list[InternalMessage]:
        return [
            message
            for message in self._direct_messages
            if message.sender_id == participant_id or message.recipient_id == participant_id
        ]
