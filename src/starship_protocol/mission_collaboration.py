from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .captain_console import CaptainCrewProposal
from .internal_comms import BlackboardEntry, InternalCommunicationsHub, InternalMessage
from .runtime import StarshipRuntime


@dataclass
class MissionCollaborationProfile:
    mission_name: str
    enabled_modes: list[str] = field(default_factory=list)
    board_names: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass
class CollaborationBootstrapResult:
    profile: MissionCollaborationProfile
    seeded_messages: list[InternalMessage] = field(default_factory=list)
    seeded_blackboard_entries: list[BlackboardEntry] = field(default_factory=list)


class MissionCollaborationCoordinator:
    """Configures and seeds communication modes for a mission-specific crew."""

    def __init__(self, runtime: StarshipRuntime) -> None:
        self.runtime = runtime
        self.internal_comms: InternalCommunicationsHub = runtime.internal_comms

    def bootstrap_for_proposal(self, proposal: CaptainCrewProposal, *, mission_name: str) -> CollaborationBootstrapResult:
        role_group_tags = {tag for role in proposal.proposed_roles for tag in role.group_tags}
        enabled_modes = self._choose_modes(role_group_tags)
        board_names = self._choose_boards(role_group_tags, mission_name)
        profile = MissionCollaborationProfile(
            mission_name=mission_name,
            enabled_modes=enabled_modes,
            board_names=board_names,
            notes=[
                "Captain selected lean mission communication modes based on proposed crew makeup.",
                f"Detected group tags: {sorted(role_group_tags)}",
            ],
        )
        result = CollaborationBootstrapResult(profile=profile)

        if "BLACKBOARD" in enabled_modes:
            for board_name in board_names:
                seeded_entry = self.internal_comms.post_blackboard_entry(
                    author_id=self.runtime.starship.captain.chameleon_id,
                    board_name=board_name,
                    content=f"Captain opened collaboration board '{board_name}' for mission '{mission_name}'.",
                    metadata={"seeded_by": "captain", "mission_name": mission_name},
                )
                result.seeded_blackboard_entries.append(seeded_entry)

        if self.runtime.starship.crew:
            first_crew_member = self.runtime.starship.crew[0]
            seeded_message = self.internal_comms.queue_mailbox_message(
                sender_id=self.runtime.starship.captain.chameleon_id,
                recipient_id=first_crew_member.chameleon_id,
                subject="initial coordination",
                content=f"Mission '{mission_name}' is active. Use the configured collaboration modes and report blockers early.",
                metadata={"seeded_by": "captain", "mission_name": mission_name},
            )
            result.seeded_messages.append(seeded_message)

        return result

    def _choose_modes(self, role_group_tags: set[str]) -> list[str]:
        enabled_modes = ["DIRECT", "MAILBOX"]
        if {"software", "art", "qa", "ops"} & role_group_tags:
            enabled_modes.append("BLACKBOARD")
        return enabled_modes

    def _choose_boards(self, role_group_tags: set[str], mission_name: str) -> list[str]:
        boards = [f"{mission_name}-captains-board"]
        if "software" in role_group_tags:
            boards.append(f"{mission_name}-software-board")
        if "art" in role_group_tags:
            boards.append(f"{mission_name}-storyboard")
        if "qa" in role_group_tags:
            boards.append(f"{mission_name}-qa-board")
        return boards
