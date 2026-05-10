from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

from starship_protocol.registry import CrewRegistry
from starship_protocol.roles import Captain, Specialist
from starship_protocol.runtime import build_runtime
from starship_protocol.viewmodel import build_captain_chat_view_model


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


def test_registry_assigns_readable_ship_ids() -> None:
    registry = CrewRegistry()
    captain = Captain(name="Captain")
    engineer = Specialist(name="Engineer", focus_area="software")

    captain_entry = registry.register(captain, role_name="captain", ship_id_prefix="captain", group_tags=["command"])
    engineer_entry = registry.register(
        engineer,
        role_name="software-engineer",
        ship_id_prefix="software-engineer",
        group_tags=["software"],
    )

    assert_true(captain_entry.ship_id == "captain-001", "captain ship id should be readable")
    assert_true(engineer_entry.ship_id == "software-engineer-001", "engineer ship id should be readable")
    assert_true(len(registry.find_by_group("software")) == 1, "software group lookup should work")


def test_viewmodel_projects_history_and_accepts_input() -> None:
    with temporary_provider_env(), TemporaryDirectory() as temporary_directory:
        runtime = build_runtime(base_path=Path(temporary_directory))
        view_model = build_captain_chat_view_model(runtime)

        initial_message_count = len(view_model.messages)
        view_model.submit_user_message("message=Captain%2C+confirm+that+the+bridge+is+ready.")

        assert_true(len(view_model.messages) >= initial_message_count + 2, "view model should project user and captain messages")
        assert_true(view_model.messages[-2].role == "user", "penultimate message should be the user")
        assert_true(view_model.messages[-1].role == "captain", "last message should be the captain")


def main() -> None:
    tests = [
        test_registry_assigns_readable_ship_ids,
        test_viewmodel_projects_history_and_accepts_input,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS all {len(tests)} registry/viewmodel tests")


if __name__ == "__main__":
    main()
