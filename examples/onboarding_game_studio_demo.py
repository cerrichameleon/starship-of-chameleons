from __future__ import annotations

import json
import sys

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from starship_protocol.engineering import ChiefEngineer
from starship_protocol.onboarding import ChameleonOnboardingCoordinator, RoleTemplate
from starship_protocol.providers import OpenClawProvider
from starship_protocol.roles import Captain, Specialist


def main() -> None:
    provider = OpenClawProvider()
    captain = Captain(name="Captain Ultra")
    chief_engineer = ChiefEngineer(name="Chief Engineer", reports_to=captain.chameleon_id)

    coordinator = ChameleonOnboardingCoordinator()
    coordinator.register_template(
        RoleTemplate(
            template_name="software-project-manager",
            focus_area="software-management",
            mission_statement="Organize the software room, consult agile best practices, and keep delivery transparent.",
            reporting_line="Captain -> Senior Software Project Manager",
            governing_documents=["software_design_document", "product_requirements_document"],
            standards=["agile_sprint_planning", "clear_status_reporting", "risk_visibility"],
            approval_path=["Captain", "Chief Engineer"],
        )
    )
    coordinator.register_template(
        RoleTemplate(
            template_name="scrum-master",
            focus_area="software-management",
            mission_statement="Facilitate standups, unblock coders, and preserve flow.",
            reporting_line="Senior Software Project Manager -> Scrum Master",
            governing_documents=["sprint_board", "task_backlog"],
            standards=["daily_standups", "blocker_tracking", "process_clarity"],
            approval_path=["Senior Software Project Manager", "Captain"],
        )
    )

    senior_project_manager = Specialist(
        name="Senior Software Project Manager",
        focus_area="software-management",
        reports_to=captain.chameleon_id,
    )
    scrum_master = Specialist(name="Scrum Master", focus_area="software-management", reports_to=captain.chameleon_id)
    ui_coder = Specialist(name="UI Coder", focus_area="software", reports_to=captain.chameleon_id)
    backend_coder = Specialist(name="Backend Coder", focus_area="software", reports_to=captain.chameleon_id)

    for chameleon, capabilities in [
        (senior_project_manager, ["planning", "management", "coordination"]),
        (scrum_master, ["planning", "facilitation", "coordination"]),
        (ui_coder, ["coding", "ui", "implementation"]),
        (backend_coder, ["coding", "backend", "implementation"]),
    ]:
        chief_engineer.outfit_with_provider(
            chameleon,
            provider,
            model_id="gpt-5.4",
            credentials_ref="env:OPENAI_API_KEY",
            capabilities=capabilities,
        )

    onboarding_records = [
        coordinator.onboard_specialist(
            senior_project_manager,
            requested_role_name="software-project-manager",
            focus_area="software-management",
            captain=captain,
            chief_engineer_name=chief_engineer.name,
            command_guidance=[
                "Organize the game studio software room for a small video game shop.",
                "Use human-legible agile practices and keep work transparent.",
            ],
        ),
        coordinator.onboard_specialist(
            scrum_master,
            requested_role_name="scrum-master",
            focus_area="software-management",
            captain=captain,
            chief_engineer_name=chief_engineer.name,
            command_guidance=[
                "Facilitate standups and blockers for the coding crew.",
                "Adapt existing scrum practices rather than reinventing process from scratch.",
            ],
        ),
        coordinator.onboard_specialist(
            ui_coder,
            requested_role_name="ui-coder",
            focus_area="software",
            captain=captain,
            chief_engineer_name=chief_engineer.name,
            command_guidance=[
                "Build the player-facing interface for the first game prototype.",
                "Follow SOLID principles, comments, and readable naming.",
            ],
        ),
        coordinator.onboard_specialist(
            backend_coder,
            requested_role_name="backend-coder",
            focus_area="software",
            captain=captain,
            chief_engineer_name=chief_engineer.name,
            command_guidance=[
                "Build gameplay logic and data/state systems for the first game prototype.",
                "Follow SOLID principles, comments, and readable naming.",
            ],
        ),
    ]

    sample_responses = {
        "project_manager": senior_project_manager.think(
            mission="organize the game studio coding crew",
            channel_status="onboarded and approved",
            user_message="Describe your role in one sentence.",
        ),
        "scrum_master": scrum_master.think(
            mission="organize the game studio coding crew",
            channel_status="onboarded and approved",
            user_message="Describe your role in one sentence.",
        ),
        "ui_coder": ui_coder.think(
            mission="build the game studio interface",
            channel_status="onboarded and approved",
            user_message="Describe your role in one sentence.",
        ),
        "backend_coder": backend_coder.think(
            mission="build the game studio backend systems",
            channel_status="onboarded and approved",
            user_message="Describe your role in one sentence.",
        ),
    }

    print(
        json.dumps(
            {
                "onboarding_records": [record.__dict__ for record in onboarding_records],
                "sample_responses": sample_responses,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
