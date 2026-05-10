from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

from starship_protocol.mission_collaboration import MissionCollaborationCoordinator
from starship_protocol.runtime import build_runtime
from starship_protocol.runtime_planner import RuntimePlanner


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


@contextmanager
def temporary_provider_env() -> None:
    names = ["OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"]
    previous = {name: os.environ.get(name) for name in names}
    os.environ["OPENAI_API_KEY"] = "sk-test-openai"
    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("GOOGLE_API_KEY", None)
    try:
        yield
    finally:
        for name, value in previous.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


def test_mission_collaboration_bootstrap_enables_blackboard_for_software_team() -> None:
    with temporary_provider_env(), TemporaryDirectory() as temporary_directory:
        runtime = build_runtime(base_path=Path(temporary_directory))
        planner = RuntimePlanner(runtime)
        proposal = runtime.captain_console.draft_crew_proposal(
            "Create a small software game studio with a software project manager, a ui coder, and a backend coder."
        )
        planner.instantiate_from_proposal(proposal)

        coordinator = MissionCollaborationCoordinator(runtime)
        bootstrap_result = coordinator.bootstrap_for_proposal(proposal, mission_name="snake-mission")

        assert_true("DIRECT" in bootstrap_result.profile.enabled_modes, "direct messaging should be enabled")
        assert_true("MAILBOX" in bootstrap_result.profile.enabled_modes, "mailbox should be enabled")
        assert_true("BLACKBOARD" in bootstrap_result.profile.enabled_modes, "software mission should enable blackboard")
        assert_true(any("software-board" in board_name for board_name in bootstrap_result.profile.board_names), "software board should be created")
        assert_true(len(bootstrap_result.seeded_blackboard_entries) >= 1, "at least one board should be seeded")
        assert_true(len(bootstrap_result.seeded_messages) == 1, "captain should seed an initial coordination message")


def main() -> None:
    tests = [test_mission_collaboration_bootstrap_enables_blackboard_for_software_team]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS all {len(tests)} mission collaboration tests")


if __name__ == "__main__":
    main()
