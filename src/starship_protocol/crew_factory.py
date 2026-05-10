from __future__ import annotations

from dataclasses import dataclass

from .captain_console import CaptainProposedRole
from .comms import Uhura
from .roles import Oxpecker, Specialist


@dataclass
class CrewFactory:
    """Creates Chameleon role instances from Captain-approved role descriptions."""

    def create_specialist(self, proposed_role: CaptainProposedRole, *, reports_to: str | None) -> Specialist:
        if "oxpecker" in proposed_role.group_tags or proposed_role.focus_area == "qa":
            return Oxpecker(name=self._display_name_from_role(proposed_role.role_name), reports_to=reports_to)
        return Specialist(
            name=self._display_name_from_role(proposed_role.role_name),
            focus_area=proposed_role.focus_area,
            reports_to=reports_to,
        )

    def create_comms_officer(
        self,
        *,
        name: str,
        reports_to: str | None,
        allowed_targets: set[str],
        audit_path,
        state_path,
    ) -> Uhura:
        return Uhura(
            name=name,
            allowed_targets=allowed_targets,
            audit_path=audit_path,
            state_path=state_path,
            reports_to=reports_to,
        )

    def _display_name_from_role(self, role_name: str) -> str:
        return role_name.replace("-", " ").replace("_", " ").title()
