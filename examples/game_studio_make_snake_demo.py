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
from starship_protocol.starship import Starship


def main() -> None:
    provider = OpenClawProvider()
    captain = Captain(name="Captain Ultra")
    chief_engineer = ChiefEngineer(name="Chief Engineer", reports_to=captain.chameleon_id)
    ship = Starship(name="Video Game Shop Starship", ship_class="game-studio", captain=captain)

    coordinator = ChameleonOnboardingCoordinator()
    coordinator.register_template(
        RoleTemplate(
            template_name="software-project-manager",
            focus_area="software-management",
            mission_statement="Organize the game crew, define work clearly, and keep status transparent.",
            reporting_line="Captain -> Senior Software Project Manager",
            governing_documents=["game_design_notes", "implementation_plan"],
            standards=["agile_planning", "clear_status_reporting", "human_legible_process"],
            approval_path=["Captain", "Chief Engineer"],
        )
    )
    coordinator.register_template(
        RoleTemplate(
            template_name="scrum-master",
            focus_area="software-management",
            mission_statement="Facilitate progress, unblock coders, and maintain team rhythm.",
            reporting_line="Senior Software Project Manager -> Scrum Master",
            governing_documents=["sprint_backlog", "task_board"],
            standards=["daily_standups", "blocker_tracking", "transparent_updates"],
            approval_path=["Senior Software Project Manager", "Captain"],
        )
    )

    game_project_manager = Specialist(
        name="Senior Software Project Manager",
        focus_area="software-management",
        reports_to=captain.chameleon_id,
    )
    scrum_master = Specialist(name="Scrum Master", focus_area="software-management", reports_to=captain.chameleon_id)
    ui_coder = Specialist(name="UI Coder", focus_area="software", reports_to=captain.chameleon_id)
    backend_coder = Specialist(name="Backend Coder", focus_area="software", reports_to=captain.chameleon_id)

    for chameleon, capabilities in [
        (captain, ["command", "planning", "ship-coordination"]),
        (chief_engineer, ["brain-outfitting", "technical-review", "architecture"]),
        (game_project_manager, ["planning", "management", "coordination"]),
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

    for crew_member in [game_project_manager, scrum_master, ui_coder, backend_coder]:
        ship.register_crew(crew_member)

    onboarding_records = [
        coordinator.onboard_specialist(
            game_project_manager,
            requested_role_name="software-project-manager",
            focus_area="software-management",
            captain=captain,
            chief_engineer_name=chief_engineer.name,
            command_guidance=[
                "Organize a tiny game studio team to build Snake overnight.",
                "Keep the process transparent and lightweight.",
            ],
        ),
        coordinator.onboard_specialist(
            scrum_master,
            requested_role_name="scrum-master",
            focus_area="software-management",
            captain=captain,
            chief_engineer_name=chief_engineer.name,
            command_guidance=[
                "Help the coders stay coordinated and remove blockers.",
                "Do not invent elaborate bureaucracy for a tiny game.",
            ],
        ),
        coordinator.onboard_specialist(
            ui_coder,
            requested_role_name="ui-coder",
            focus_area="software",
            captain=captain,
            chief_engineer_name=chief_engineer.name,
            command_guidance=[
                "Handle player input, screen drawing, and game presentation for Snake.",
                "Use clear comments and readable names.",
            ],
        ),
        coordinator.onboard_specialist(
            backend_coder,
            requested_role_name="backend-coder",
            focus_area="software",
            captain=captain,
            chief_engineer_name=chief_engineer.name,
            command_guidance=[
                "Handle game loop, collision, score, and food spawning for Snake.",
                "Use clear comments and readable names.",
            ],
        ),
    ]

    captain_summary = captain.think(
        mission="deliver a tiny playable Snake game",
        channel_status="bridge overseeing game studio crew",
        user_message="Summarize how you will use the onboarded crew to deliver a tiny playable Snake game.",
    )
    ui_reply = ship.delegate(
        focus_area="software",
        title="snake-ui",
        description="Describe the UI responsibilities for a tiny terminal Snake game.",
    )
    backend_reply = backend_coder.think(
        mission="deliver a tiny playable Snake game",
        channel_status="backend bay active",
        user_message="Describe the backend/gameplay responsibilities for a tiny terminal Snake game.",
    )

    snake_file = Path(__file__).resolve().parent / "snake_game.py"

    print(
        json.dumps(
            {
                "captain_summary": captain_summary,
                "onboarding_records": [record.__dict__ for record in onboarding_records],
                "delegated_ui_reply": ui_reply,
                "backend_reply": backend_reply,
                "playable_game_file": str(snake_file),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
