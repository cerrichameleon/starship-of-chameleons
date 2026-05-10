from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

from starship_protocol.providers import AgentSpec, OpenClawProvider
from starship_protocol.runtime import build_runtime


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


def test_runtime_exposes_captain_console_and_chat_flow() -> None:
    with temporary_provider_env(), TemporaryDirectory() as temporary_directory:
        runtime = build_runtime(base_path=Path(temporary_directory))
        reply = runtime.captain_console.submit_chat_message("Captain, confirm bridge continuity.")

        assert_true(isinstance(reply, str) and len(reply) > 0, "captain console should return a reply")
        assert_true(len(runtime.captain_console.summarize_chat_history()) >= 2, "chat history should include both sides")


def test_captain_console_can_draft_crew_proposal() -> None:
    with temporary_provider_env(), TemporaryDirectory() as temporary_directory:
        runtime = build_runtime(base_path=Path(temporary_directory))
        proposal = runtime.captain_console.draft_crew_proposal(
            "Create a small t-shirt shop management company with sensible initial roles."
        )

        assert_true(proposal.mission_prompt.startswith("Create a small t-shirt shop"), "proposal should retain mission prompt")
        assert_true(proposal.approval_status == "draft", "new proposal should begin as a draft")
        assert_true(isinstance(proposal.rationale, str) and len(proposal.rationale) > 0, "proposal should include rationale")
        assert_true(len(proposal.proposed_roles) >= 1, "proposal should include at least one structured proposed role")


def test_provider_specific_direct_api_endpoints_are_distinct() -> None:
    openai_brain = OpenClawProvider(provider_id="openai-api").create_captain_brain(
        AgentSpec(
            role_name="captain",
            provider_id="openai-api",
            model_id="gpt-5.4",
            credentials_ref="env:OPENAI_API_KEY",
        )
    )
    gemini_brain = OpenClawProvider(provider_id="gemini-api").create_captain_brain(
        AgentSpec(
            role_name="captain",
            provider_id="gemini-api",
            model_id="gemini-2.5-pro",
            credentials_ref="env:GEMINI_API_KEY",
        )
    )

    assert_true(openai_brain.config.endpoint == "https://api.openai.com/v1/responses", "OpenAI path should keep the OpenAI responses endpoint")
    assert_true(
        gemini_brain.config.endpoint == "https://generativelanguage.googleapis.com/v1beta/openai/responses",
        "Gemini path should use the Gemini-compatible responses endpoint instead of OpenAI's endpoint",
    )


def main() -> None:
    tests = [
        test_runtime_exposes_captain_console_and_chat_flow,
        test_captain_console_can_draft_crew_proposal,
        test_provider_specific_direct_api_endpoints_are_distinct,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS all {len(tests)} runtime console tests")


if __name__ == "__main__":
    main()
