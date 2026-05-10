from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

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


def test_internal_comms_supports_direct_mailbox_and_blackboard() -> None:
    with temporary_provider_env(), TemporaryDirectory() as temporary_directory:
        runtime = build_runtime(base_path=Path(temporary_directory))
        planner = RuntimePlanner(runtime)
        proposal = runtime.captain_console.draft_crew_proposal(
            "Create a small software game studio with a software project manager, a ui coder, and a backend coder."
        )
        result = planner.instantiate_from_proposal(proposal)

        assert_true(len(result.instantiated_roles) >= 1, "need at least one instantiated role for comms test")
        sender = runtime.starship.crew[0]
        recipient = runtime.starship.crew[-1]

        direct_message = runtime.internal_comms.send_direct_message(
            sender_id=sender.chameleon_id,
            recipient_id=recipient.chameleon_id,
            subject="coordination",
            content="Please confirm your current task scope.",
        )
        mailbox_message = runtime.internal_comms.queue_mailbox_message(
            sender_id=sender.chameleon_id,
            recipient_id=recipient.chameleon_id,
            subject="handoff",
            content="Queued follow-up for later review.",
        )
        blackboard_entry = runtime.internal_comms.post_blackboard_entry(
            author_id=sender.chameleon_id,
            board_name="snake-mission-board",
            content="Initial gameplay responsibilities and notes.",
        )

        assert_true(direct_message.recipient_id == recipient.chameleon_id, "direct message should target recipient")
        assert_true(len(runtime.internal_comms.read_mailbox(recipient.chameleon_id)) == 1, "mailbox should contain queued message")
        assert_true(len(runtime.internal_comms.read_blackboard("snake-mission-board")) == 1, "blackboard should contain entry")
        assert_true(blackboard_entry.board_name == "snake-mission-board", "blackboard entry should retain board name")


def main() -> None:
    tests = [test_internal_comms_supports_direct_mailbox_and_blackboard]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS all {len(tests)} internal comms tests")


if __name__ == "__main__":
    main()
