from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .roles import Captain, Specialist


class OnboardingMode(str, Enum):
    FULL = "FULL"
    ADAPT = "ADAPT"
    REUSE = "REUSE"


@dataclass
class RoleTemplate:
    template_name: str
    focus_area: str
    mission_statement: str
    reporting_line: str
    governing_documents: list[str] = field(default_factory=list)
    standards: list[str] = field(default_factory=list)
    approval_path: list[str] = field(default_factory=list)


@dataclass
class OnboardingRecord:
    chameleon_name: str
    requested_role_name: str
    onboarding_mode: OnboardingMode
    command_guidance: list[str]
    drafted_identity: str
    captain_feedback: str
    engineer_feedback: str
    approved: bool
    adopted_template_name: str | None = None


class ChameleonOnboardingCoordinator:
    def __init__(self) -> None:
        self.templates: dict[str, RoleTemplate] = {}

    def register_template(self, template: RoleTemplate) -> None:
        self.templates[template.template_name] = template

    def onboard_specialist(
        self,
        specialist: Specialist,
        *,
        requested_role_name: str,
        focus_area: str,
        captain: Captain,
        chief_engineer_name: str,
        command_guidance: list[str],
    ) -> OnboardingRecord:
        template = self.templates.get(requested_role_name)
        onboarding_mode = OnboardingMode.FULL if template is None else OnboardingMode.REUSE

        drafted_identity = self._draft_identity(
            specialist=specialist,
            requested_role_name=requested_role_name,
            focus_area=focus_area,
            chief_engineer_name=chief_engineer_name,
            command_guidance=command_guidance,
            template=template,
        )
        captain_feedback = self._captain_feedback(captain, requested_role_name, template)
        engineer_feedback = self._engineer_feedback(chief_engineer_name, requested_role_name, template)

        approved = True
        specialist.receive_directive(
            "When assigned a role, I will work with command to confirm my function. If an approved role definition already exists, I will reuse and adapt it before creating a new one."
        )
        specialist.receive_directive(drafted_identity)
        specialist.focus_area = focus_area

        return OnboardingRecord(
            chameleon_name=specialist.name,
            requested_role_name=requested_role_name,
            onboarding_mode=onboarding_mode,
            command_guidance=command_guidance,
            drafted_identity=drafted_identity,
            captain_feedback=captain_feedback,
            engineer_feedback=engineer_feedback,
            approved=approved,
            adopted_template_name=template.template_name if template else None,
        )

    def _draft_identity(
        self,
        *,
        specialist: Specialist,
        requested_role_name: str,
        focus_area: str,
        chief_engineer_name: str,
        command_guidance: list[str],
        template: RoleTemplate | None,
    ) -> str:
        if template:
            return (
                f"I am {specialist.name}, serving as {requested_role_name}. "
                f"I adopt the approved role pattern '{template.template_name}' and adapt it to current mission needs. "
                f"I report through {template.reporting_line}, follow {', '.join(template.standards)}, "
                f"consult {', '.join(template.governing_documents)}, and coordinate with {chief_engineer_name}. "
                f"Additional command guidance: {'; '.join(command_guidance)}."
            )
        return (
            f"I am {specialist.name}, serving as {requested_role_name} in focus area '{focus_area}'. "
            f"I will engage with command to refine this role until it is clearly agreed. "
            f"I will study the relevant best practices for this profession, follow SOLID and separation of concerns where software is involved, "
            f"report through the designated chain of command, and use these command constraints as governing guidance: {'; '.join(command_guidance)}."
        )

    def _captain_feedback(self, captain: Captain, requested_role_name: str, template: RoleTemplate | None) -> str:
        if template:
            return (
                f"Captain {captain.name} approves reuse of the established '{requested_role_name}' role pattern. "
                "Proceed and adapt only where mission needs differ."
            )
        return (
            f"Captain {captain.name} approves the drafted role definition for {requested_role_name}. "
            "Proceed and keep command informed if the role needs refinement."
        )

    def _engineer_feedback(self, chief_engineer_name: str, requested_role_name: str, template: RoleTemplate | None) -> str:
        if template:
            return (
                f"{chief_engineer_name} confirms the existing template is suitable and should be reused for {requested_role_name}."
            )
        return (
            f"{chief_engineer_name} confirms the role definition is technically coherent and aligned with current best practices for {requested_role_name}."
        )
