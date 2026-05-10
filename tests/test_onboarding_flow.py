from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from starship_protocol.brain_selection import detect_provider_readiness, select_brain_for_launch
from starship_protocol.captain_chat import CaptainConversationTurn
from starship_protocol.onboarding_ui import build_onboarding_screen_view_model
from starship_protocol.web_ui import StarshipWebHandler


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


@contextmanager
def isolated_provider_env():
    names = ["OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY", "STARSHIP_PROVIDER_CREDENTIALS_FILE"]
    previous = {name: os.environ.get(name) for name in names}
    try:
        for name in names:
            os.environ.pop(name, None)
        yield
    finally:
        for name, value in previous.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


@contextmanager
def temporary_cwd(path: Path):
    previous_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous_cwd)


def test_onboarding_gates_until_any_provider_is_ready() -> None:
    with isolated_provider_env(), TemporaryDirectory() as temporary_directory:
        view_model = build_onboarding_screen_view_model(Path(temporary_directory))

        assert_true(view_model.should_gate_to_onboarding(), "without ready providers the launch should stay gated")
        assert_true(view_model.current_step == "select", "default step should start at selection")
        assert_true(not detect_provider_readiness()["openai-api"]["ready"], "clean isolated env should not leak OpenAI readiness")

        view_model.submit_provider_selection("provider=openai-api")
        assert_true(view_model.current_step == "setup", "selection should move into setup")
        assert_true(view_model.should_gate_to_onboarding(), "selection alone should still stay gated until readiness exists")


def test_onboarding_persists_api_key_for_readiness_and_launch() -> None:
    with isolated_provider_env(), TemporaryDirectory() as temporary_directory:
        base_path = Path(temporary_directory)
        with temporary_cwd(base_path):
            view_model = build_onboarding_screen_view_model(base_path)

            view_model.submit_provider_selection("provider=openai-api")
            view_model.submit_provider_setup("provider_id=openai-api&api_key=sk-persisted")

            credentials_path = base_path / "var" / "provider_credentials.json"
            assert_true(credentials_path.exists(), "provider credentials file should be written for API-key providers")
            assert_true(view_model.provider_setups["openai-api"].severity == "green", "saved API key should surface as ready")
            assert_true(
                detect_provider_readiness()["openai-api"]["ready"],
                "readiness detection should pick up the saved provider credentials file",
            )
            assert_true(
                select_brain_for_launch(view_model.get_launch_policy()).provider_id == "openai-api",
                "launch selection should use the saved onboarding credential",
            )


def test_onboarding_persists_gemini_key_for_readiness_and_launch() -> None:
    with isolated_provider_env(), TemporaryDirectory() as temporary_directory:
        base_path = Path(temporary_directory)
        with temporary_cwd(base_path):
            view_model = build_onboarding_screen_view_model(base_path)

            view_model.submit_provider_selection("provider=gemini-api")
            view_model.submit_provider_setup("provider_id=gemini-api&api_key=gemini-secret")

            credentials_path = base_path / "var" / "provider_credentials.json"
            assert_true(credentials_path.exists(), "provider credentials file should be written for Gemini API as well")
            assert_true(view_model.provider_setups["gemini-api"].severity == "green", "saved Gemini key should surface as ready")
            assert_true(
                detect_provider_readiness()["gemini-api"]["ready"],
                "readiness detection should pick up the saved Gemini credentials file",
            )
            assert_true(
                select_brain_for_launch(view_model.get_launch_policy()).provider_id == "gemini-api",
                "launch selection should use the saved Gemini onboarding credential",
            )


def test_onboarding_persists_ready_state_and_allows_console() -> None:
    with isolated_provider_env(), TemporaryDirectory() as temporary_directory:
        base_path = Path(temporary_directory)
        state_path = base_path / "var" / "onboarding_state.json"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            """
{
  "selected_provider_ids": ["openai-api"],
  "active_provider_id": null,
  "current_step": "monitor",
  "provider_setups": {
    "openai-api": {
      "status": "ready",
      "severity": "green",
      "readiness_detail": "API key detected and ready for launch.",
      "api_key_value": "sk-ready"
    }
  }
}
""".strip()
            + "\n"
        )

        view_model = build_onboarding_screen_view_model(base_path)
        assert_true(not view_model.should_gate_to_onboarding(), "ready provider should allow console access")
        assert_true(view_model.current_step == "monitor", "ready provider should land on monitor state")


def test_fresh_chat_flag_resets_captain_conversation() -> None:
    handler = StarshipWebHandler.__new__(StarshipWebHandler)
    resets: list[str] = []
    fake_session = SimpleNamespace(
        history=[CaptainConversationTurn(role="user", text="old message")],
        reset_conversation=lambda: resets.append("reset"),
    )
    handler.path = "/?tab=chat&fresh=1"
    handler.onboarding_view_model = SimpleNamespace(refresh_readiness=lambda: None, should_gate_to_onboarding=lambda: False)
    handler.view_model = SimpleNamespace(
        runtime=SimpleNamespace(captain_chat_session=fake_session),
        active_tab="chat",
        refresh=lambda: None,
        chat_tab=SimpleNamespace(
            title="Captain",
            subtitle="Bridge",
            startup_manifest_lines=[],
            messages=[],
            placeholder_text="Say something",
            send_button_text="Send",
        ),
        monitor_tab=SimpleNamespace(tick_count=0, last_tick_at=None, crew_entries=[]),
    )
    sent = []
    headers = []
    handler.send_response = lambda code: sent.append(code)
    handler.send_header = lambda key, value: headers.append((key, value))
    handler.end_headers = lambda: None
    handler.wfile = SimpleNamespace(write=lambda body: None)

    handler.do_GET()

    assert_true(resets == ["reset"], "fresh=1 should reset the Captain conversation before rendering chat")
    assert_true(sent == [200], "fresh chat request should render successfully")


def main() -> None:
    tests = [
        test_onboarding_gates_until_any_provider_is_ready,
        test_onboarding_persists_api_key_for_readiness_and_launch,
        test_onboarding_persists_gemini_key_for_readiness_and_launch,
        test_onboarding_persists_ready_state_and_allows_console,
        test_fresh_chat_flag_resets_captain_conversation,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS all {len(tests)} onboarding flow tests")


if __name__ == "__main__":
    main()
