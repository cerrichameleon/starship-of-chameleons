from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

from starship_protocol.engineering import ChiefEngineer
from starship_protocol.onboarding import ChameleonOnboardingCoordinator, RoleTemplate
from starship_protocol.providers import OpenClawProvider
from starship_protocol.roles import Captain, Specialist
from starship_protocol.starship import Starship


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def main() -> None:
    workspace_root = Path(__file__).resolve().parents[1]
    mission_root = workspace_root / "examples" / "starship_workflows" / "snake_mission"
    docs_root = mission_root / "docs"
    logs_root = mission_root / "logs"

    provider = OpenClawProvider()
    captain = Captain(name="Captain Ultra")
    chief_engineer = ChiefEngineer(name="Chief Engineer", reports_to=captain.chameleon_id)
    ship = Starship(name="Starship of Chameleons", ship_class="software-factory", captain=captain)

    software_project_manager = Specialist(
        name="Software Project Manager",
        focus_area="software-management",
        reports_to=captain.chameleon_id,
    )
    coder_one = Specialist(name="Coder One", focus_area="software", reports_to=captain.chameleon_id)
    coder_two = Specialist(name="Coder Two", focus_area="software", reports_to=captain.chameleon_id)

    for crew_member, capabilities in [
        (captain, ["command", "mission-oversight", "delegation"]),
        (chief_engineer, ["brain-outfitting", "technical-review", "architecture"]),
        (software_project_manager, ["planning", "requirements", "task-breakdown", "documentation"]),
        (coder_one, ["python", "game-logic", "unit-testing", "git"]),
        (coder_two, ["python", "rendering", "integration", "git"]),
    ]:
        chief_engineer.outfit_with_provider(
            crew_member,
            provider,
            model_id="gpt-5.4",
            credentials_ref="auth-profile:openai-codex:mattcleere@gmail.com",
            capabilities=capabilities,
        )

    for crew_member in [software_project_manager, coder_one, coder_two]:
        ship.register_crew(crew_member)

    onboarding = ChameleonOnboardingCoordinator()
    onboarding.register_template(
        RoleTemplate(
            template_name="software-project-manager",
            focus_area="software-management",
            mission_statement="Translate product intent into organized software work.",
            reporting_line="Captain -> Software Project Manager",
            governing_documents=["game_design_document", "software_design_document", "requirements_and_task_breakdown"],
            standards=["documentation_first", "small_commits", "transparent_status"],
            approval_path=["Captain", "Chief Engineer"],
        )
    )

    onboarding_records = [
        onboarding.onboard_specialist(
            software_project_manager,
            requested_role_name="software-project-manager",
            focus_area="software-management",
            captain=captain,
            chief_engineer_name=chief_engineer.name,
            command_guidance=[
                "Produce a proper GDD and SDD for Snake.",
                "Split work between two coders and keep the version-control trail clean.",
            ],
        ),
        onboarding.onboard_specialist(
            coder_one,
            requested_role_name="snake-game-logic-coder",
            focus_area="software",
            captain=captain,
            chief_engineer_name=chief_engineer.name,
            command_guidance=[
                "Own the model, gameplay rules, and unit tests.",
                "Do not tangle gameplay logic with the terminal view.",
            ],
        ),
        onboarding.onboard_specialist(
            coder_two,
            requested_role_name="snake-game-runtime-coder",
            focus_area="software",
            captain=captain,
            chief_engineer_name=chief_engineer.name,
            command_guidance=[
                "Own controls, rendering, runtime orchestration, and integration.",
                "Keep the human play loop responsive and readable.",
            ],
        ),
    ]

    mission_brief = dedent(
        """
        Mission: deliver the first true Starship-run software mission.
        Product: a tiny playable Snake game.
        Required human-style process: GDD, SDD, task breakdown, two coder assignments, unit tests, and version-control discipline.
        Workspace: examples/starship_workflows/snake_mission
        """
    ).strip()

    captain_order = captain.think(
        mission="execute a real Starship first run for the Snake mission",
        channel_status="bridge active",
        user_message=mission_brief,
    )
    project_manager_plan = software_project_manager.think(
        mission="plan and supervise the Snake mission",
        channel_status="project management office active",
        user_message=(
            "Read the mission brief and produce a concise management plan, including how work should be divided between two coders "
            "using version control and documentation-first practices."
        ),
    )
    coder_one_plan = coder_one.think(
        mission="implement the model and tests for Snake",
        channel_status="logic bay active",
        user_message=(
            "State your implementation plan for the model layer and unit tests for Snake. "
            "Focus on state, movement, food, scoring, collision, and testability."
        ),
    )
    coder_two_plan = coder_two.think(
        mission="implement the runtime and rendering for Snake",
        channel_status="runtime bay active",
        user_message=(
            "State your implementation plan for controls, rendering, and runtime integration for Snake. "
            "Assume the model layer is separate and should remain reusable for testing."
        ),
    )
    captain_review = captain.think(
        mission="review the first Starship Snake mission run",
        channel_status="bridge review mode",
        user_message=(
            "Review the mission outputs and state whether this counts as a successful first Starship run. "
            "Comment on documentation, crew structure, testability, real-brain usage, and next gaps to close."
        ),
    )

    write_text(
        logs_root / "starship_first_run_summary.md",
        f"""
        # Starship First Run Summary

        ## Captain Initial Order
        {captain_order}

        ## Software Project Manager Plan
        {project_manager_plan}

        ## Coder One Plan
        {coder_one_plan}

        ## Coder Two Plan
        {coder_two_plan}

        ## Captain Final Review
        {captain_review}
        """,
    )

    write_text(
        logs_root / "starship_onboarding_records.json",
        json.dumps([record.__dict__ for record in onboarding_records], indent=2),
    )

    status_payload = {
        "success": True,
        "workspace": str(mission_root),
        "captain_has_brain": captain.has_brain(),
        "project_manager_has_brain": software_project_manager.has_brain(),
        "coder_one_has_brain": coder_one.has_brain(),
        "coder_two_has_brain": coder_two.has_brain(),
        "generated_files": [
            str(docs_root / "game_design_document.md"),
            str(docs_root / "software_design_document.md"),
            str(docs_root / "requirements_and_task_breakdown.md"),
            str(logs_root / "mission_log.md"),
            str(logs_root / "crew_status_report.md"),
            str(logs_root / "test_results.txt"),
            str(logs_root / "starship_first_run_summary.md"),
            str(logs_root / "starship_onboarding_records.json"),
        ],
    }
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
