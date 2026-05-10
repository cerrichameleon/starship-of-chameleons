from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from .captain_console import CaptainCrewProposal, CaptainProposedRole
from .onboarding import ChameleonOnboardingCoordinator
from .providers import OpenClawProvider
from .roles import Specialist
from .runtime import StarshipRuntime


@dataclass
class PlannedCrewRole:
    role_name: str
    ship_id_prefix: str
    focus_area: str
    group_tags: list[str] = field(default_factory=list)
    reports_to_role_name: str | None = None


@dataclass
class CrewInstantiationResult:
    proposal: CaptainCrewProposal
    instantiated_roles: list[dict[str, Any]] = field(default_factory=list)


class RuntimePlanner:
    """Turns Captain proposals into instantiated Starship crew using backend protocols."""

    def __init__(self, runtime: StarshipRuntime) -> None:
        self.runtime = runtime
        self.onboarding = ChameleonOnboardingCoordinator()
        captain_profile = runtime.starship.captain.brain_profile
        self.provider = OpenClawProvider(provider_id=str(captain_profile.get("provider_id", "openai-api")))

    def instantiate_from_proposal(self, proposal: CaptainCrewProposal) -> CrewInstantiationResult:
        planned_roles = self._infer_roles_from_proposal(proposal)
        chief_engineer = self.runtime.starship.chief_engineer
        if chief_engineer is None:
            raise RuntimeError("Starship has no Chief Engineer available for brain outfitting")
        captain_profile = self.runtime.starship.captain.brain_profile
        model_id = str(captain_profile.get("model_id", "gpt-5.4"))
        credentials_ref = str(captain_profile.get("credentials_ref", "env:OPENAI_API_KEY"))

        result = CrewInstantiationResult(proposal=proposal)
        created_by_role_name: dict[str, Specialist] = {}
        for planned_role in planned_roles:
            reports_to_id = self._resolve_reports_to_id(planned_role.reports_to_role_name, created_by_role_name)
            specialist = self.runtime.crew_factory.create_specialist(
                CaptainProposedRole(
                    role_name=planned_role.role_name,
                    reason="runtime planner instantiation",
                    focus_area=planned_role.focus_area,
                    group_tags=list(planned_role.group_tags),
                    reports_to_role_name=planned_role.reports_to_role_name,
                ),
                reports_to=reports_to_id,
            )
            self.onboarding.onboard_specialist(
                specialist,
                requested_role_name=planned_role.role_name,
                focus_area=planned_role.focus_area,
                captain=self.runtime.starship.captain,
                chief_engineer_name=chief_engineer.name,
                command_guidance=[
                    f"Mission prompt: {proposal.mission_prompt}",
                    f"Captain rationale: {proposal.rationale}",
                ],
            )
            chief_engineer.outfit_with_provider(
                specialist,
                self.provider,
                model_id=model_id,
                credentials_ref=credentials_ref,
                capabilities=[planned_role.focus_area, "crew-duty", "execution"],
            )
            registry_entry = self.runtime.starship.register_crew(
                specialist,
                role_name=planned_role.role_name,
                ship_id_prefix=planned_role.ship_id_prefix,
                group_tags=planned_role.group_tags,
            )
            created_by_role_name[planned_role.role_name] = specialist
            result.instantiated_roles.append(
                {
                    "role_name": planned_role.role_name,
                    "ship_id": registry_entry.ship_id,
                    "focus_area": planned_role.focus_area,
                    "group_tags": list(planned_role.group_tags),
                    "reports_to": planned_role.reports_to_role_name,
                    "has_brain": specialist.has_brain(),
                }
            )
        proposal.approval_status = "instantiated"
        return result

    def _infer_roles_from_proposal(self, proposal: CaptainCrewProposal) -> list[PlannedCrewRole]:
        if proposal.proposed_roles:
            return [self._planned_role_from_proposed_role(proposed_role) for proposed_role in proposal.proposed_roles]
        return [
            PlannedCrewRole(
                role_name="general-specialist",
                ship_id_prefix="general-specialist",
                focus_area="general",
                group_tags=["general"],
                reports_to_role_name=None,
            )
        ]

    def _planned_role_from_proposed_role(self, proposed_role: CaptainProposedRole) -> PlannedCrewRole:
        normalized_role_name = proposed_role.role_name.replace(" ", "-")
        return PlannedCrewRole(
            role_name=normalized_role_name,
            ship_id_prefix=normalized_role_name,
            focus_area=proposed_role.focus_area,
            group_tags=list(proposed_role.group_tags),
            reports_to_role_name=proposed_role.reports_to_role_name,
        )

    def _resolve_reports_to_id(self, reports_to_role_name: str | None, created_by_role_name: dict[str, Specialist]) -> str | None:
        if not reports_to_role_name:
            return self.runtime.starship.captain.chameleon_id
        report_target = created_by_role_name.get(reports_to_role_name)
        if report_target is None:
            return self.runtime.starship.captain.chameleon_id
        return report_target.chameleon_id

    def _display_name_from_role(self, role_name: str) -> str:
        return re.sub(r"[-_]", " ", role_name).title()
