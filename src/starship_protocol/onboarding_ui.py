from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import parse_qs
import json
import os

from .brain_selection import LaunchPolicy, detect_provider_readiness


PROVIDER_ENV_KEYS = {
    "openai-api": "OPENAI_API_KEY",
    "gemini-api": "GEMINI_API_KEY",
}


@dataclass
class ProviderOptionViewData:
    provider_id: str
    label: str
    description: str


@dataclass
class ProviderSetupViewData:
    provider_id: str
    label: str
    status: str = "not-started"
    severity: str = "red"
    readiness_detail: str = "Not checked yet."
    needs_api_key: bool = False
    needs_oauth: bool = False
    api_key_value: str = ""
    help_sections: dict[str, str] = field(default_factory=dict)


@dataclass
class OnboardingScreenViewModel:
    state_path: Path
    selected_provider_ids: list[str] = field(default_factory=list)
    active_provider_id: str | None = None
    provider_options: list[ProviderOptionViewData] = field(default_factory=list)
    provider_setups: dict[str, ProviderSetupViewData] = field(default_factory=dict)
    current_step: str = "select"
    continue_after_first_success: bool = True

    def __post_init__(self) -> None:
        self.provider_options = [
            ProviderOptionViewData(
                provider_id="openai-api",
                label="ChatGPT 5.4 API",
                description="API key path for OpenAI's standard API billing.",
            ),
            ProviderOptionViewData(
                provider_id="codex-oauth",
                label="ChatGPT Codex",
                description="ChatGPT login path, with browser sign-in or device code fallback.",
            ),
            ProviderOptionViewData(
                provider_id="gemini-api",
                label="Gemini API",
                description="Google Gemini API key path.",
            ),
        ]
        self.provider_setups = {
            "openai-api": ProviderSetupViewData(
                provider_id="openai-api",
                label="ChatGPT 5.4 API",
                status="not-started",
                needs_api_key=True,
                help_sections={
                    "missing-subscription": (
                        "1. Go to https://platform.openai.com/\n"
                        "2. Sign in to your OpenAI account.\n"
                        "3. Set up billing if OpenAI requires it.\n"
                        "4. Stay logged in and continue to create an API key."
                    ),
                    "find-key": (
                        "1. Go to https://platform.openai.com/\n"
                        "2. Open the API keys section.\n"
                        "3. Click Create new secret key.\n"
                        "4. Copy it immediately and paste it back here."
                    ),
                },
            ),
            "codex-oauth": ProviderSetupViewData(
                provider_id="codex-oauth",
                label="ChatGPT Codex",
                status="not-started",
                needs_oauth=True,
                help_sections={
                    "why-human": (
                        "Codex needs a one-time human login. OpenAI may ask for password, MFA, text code, or other account verification. Starship should use Codex's own auth file, not OpenClaw's saved profile."
                    ),
                    "steps": (
                        "1. Open https://developers.openai.com/codex/auth and follow the Codex login instructions, or run codex login on the host if that is the supported local path.\n"
                        "2. Sign in to the OpenAI account you want to use.\n"
                        "3. Complete any MFA or account verification step OpenAI asks for.\n"
                        "4. If browser-driven login is awkward, run codex login --device-auth instead.\n"
                        "5. If this machine is headless, log in once on a machine with a browser and copy ~/.codex/auth.json onto the target machine."
                    ),
                },
            ),
            "gemini-api": ProviderSetupViewData(
                provider_id="gemini-api",
                label="Gemini API",
                status="not-started",
                needs_api_key=True,
                help_sections={
                    "missing-subscription": (
                        "1. Go to https://aistudio.google.com/\n"
                        "2. Sign in with your Google account.\n"
                        "3. Accept any Google AI Studio terms if they appear.\n"
                        "4. Stay logged in and continue to create a Gemini API key."
                    ),
                    "find-key": (
                        "1. In Google AI Studio, open Get API key or the API keys page.\n"
                        "2. Create a Gemini API key for the project Google gives you, or for the project you choose.\n"
                        "3. Copy it immediately and paste it back here."
                    ),
                },
            ),
        }
        self._load_state()
        self.refresh_readiness()

    def refresh_readiness(self) -> None:
        readiness_by_provider = detect_provider_readiness()
        for provider_id, setup in self.provider_setups.items():
            readiness = readiness_by_provider.get(provider_id)
            if not readiness:
                continue
            detected_status = str(readiness.get("status", setup.status))
            detected_severity = str(readiness.get("severity", setup.severity))
            detected_detail = str(readiness.get("detail", setup.readiness_detail))
            if setup.severity == "green":
                continue
            if setup.severity == "yellow" and setup.api_key_value and detected_severity != "green":
                continue
            setup.status = detected_status
            setup.severity = detected_severity
            setup.readiness_detail = detected_detail
        self._derive_step_from_readiness()
        self._save_state()

    def should_gate_to_onboarding(self) -> bool:
        if not self.selected_provider_ids:
            return True
        return self.current_step != "monitor" or not self.has_ready_provider()

    def has_ready_provider(self) -> bool:
        return any(self.provider_setups[provider_id].severity == "green" for provider_id in self.selected_provider_ids)

    def submit_provider_selection(self, raw_form_body: str) -> None:
        parsed_form = parse_qs(raw_form_body, keep_blank_values=True)
        ordered_ids = [item.strip() for item in parsed_form.get("provider_order", [""])[0].split(",") if item.strip()]
        selected_ids = set(parsed_form.get("provider", []))
        if ordered_ids:
            self.selected_provider_ids = [provider_id for provider_id in ordered_ids if provider_id in selected_ids]
        else:
            self.selected_provider_ids = parsed_form.get("provider", [])
        self.continue_after_first_success = parsed_form.get("continue_mode", ["all"])[0] != "first-success"
        if not self.selected_provider_ids:
            self.current_step = "select"
            self.refresh_readiness()
            return
        self.active_provider_id = self.selected_provider_ids[0]
        self.current_step = "setup"
        self._save_state()

    def submit_provider_setup(self, raw_form_body: str) -> None:
        parsed_form = parse_qs(raw_form_body, keep_blank_values=True)
        provider_id = parsed_form.get("provider_id", [""])[0]
        if provider_id not in self.provider_setups:
            return
        setup = self.provider_setups[provider_id]
        continue_mode = parsed_form.get("continue_mode", ["all"])[0]
        self.continue_after_first_success = continue_mode != "first-success"
        if setup.needs_api_key:
            setup.api_key_value = parsed_form.get("api_key", [""])[0].strip()
            setup.status = "key-entered" if setup.api_key_value else "needs-setup"
            setup.severity = "yellow" if setup.api_key_value else "red"
            setup.readiness_detail = (
                "Key entered in the form. Starship will persist it to var/provider_credentials.json so runtime detection can verify readiness."
                if setup.api_key_value
                else "No API key entered yet."
            )
        elif setup.needs_oauth:
            setup.status = "waiting-for-oauth"
            setup.severity = "yellow"
            setup.readiness_detail = "Waiting for the one-time human login and reusable local Codex auth state to exist."
        self._persist_provider_entry(setup)
        self.refresh_readiness()
        self._advance_to_next_provider(provider_id)

    def _advance_to_next_provider(self, provider_id: str) -> None:
        current_setup = self.provider_setups.get(provider_id)
        if current_setup and current_setup.severity == "green" and not self.continue_after_first_success:
            self.active_provider_id = None
            self.current_step = "monitor"
            self._save_state()
            return
        try:
            current_index = self.selected_provider_ids.index(provider_id)
        except ValueError:
            self.current_step = "monitor"
            return
        next_index = current_index + 1
        if next_index >= len(self.selected_provider_ids):
            self.active_provider_id = None
            self.current_step = "monitor"
            self._save_state()
            return
        self.active_provider_id = self.selected_provider_ids[next_index]
        self.current_step = "setup"
        self._save_state()

    def _derive_step_from_readiness(self) -> None:
        ready_selected = [
            provider_id
            for provider_id in self.selected_provider_ids
            if self.provider_setups.get(provider_id) and self.provider_setups[provider_id].severity == "green"
        ]
        pending_selected = [
            provider_id
            for provider_id in self.selected_provider_ids
            if self.provider_setups.get(provider_id) and self.provider_setups[provider_id].severity != "green"
        ]
        if ready_selected and (not pending_selected or not self.continue_after_first_success):
            self.current_step = "monitor"
            self.active_provider_id = None
            return
        if pending_selected:
            self.current_step = "setup"
            self.active_provider_id = pending_selected[0]
            return
        if self.has_ready_provider() and self.selected_provider_ids:
            self.current_step = "monitor"
            self.active_provider_id = None
            return
        self.current_step = "select"
        self.active_provider_id = None

    def get_launch_policy(self) -> LaunchPolicy:
        provider_order: list[str] = []
        for provider_id in self.selected_provider_ids:
            if provider_id == "codex-oauth":
                provider_order.append("codex")
            else:
                provider_order.append(provider_id)
        return LaunchPolicy(provider_order=provider_order)

    def reset_onboarding(self) -> None:
        self.selected_provider_ids = []
        self.active_provider_id = None
        self.current_step = "select"
        self.continue_after_first_success = True
        for setup in self.provider_setups.values():
            setup.status = "not-started"
            setup.severity = "red"
            setup.readiness_detail = "Not checked yet."
            setup.api_key_value = ""
        if self.state_path.exists():
            self.state_path.unlink()
        self._save_state()

    def _persist_provider_entry(self, setup: ProviderSetupViewData) -> None:
        provider_env_key = PROVIDER_ENV_KEYS.get(setup.provider_id)
        if not provider_env_key:
            return

        credentials_path = self.state_path.parent / "provider_credentials.json"
        credentials_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            payload = json.loads(credentials_path.read_text()) if credentials_path.exists() else {}
        except Exception:
            payload = {}
        if not isinstance(payload, dict):
            payload = {}

        if setup.api_key_value:
            payload[provider_env_key] = setup.api_key_value
            os.environ[provider_env_key] = setup.api_key_value
        else:
            payload.pop(provider_env_key, None)
            os.environ.pop(provider_env_key, None)

        if payload:
            credentials_path.write_text(json.dumps(payload, indent=2) + "\n")
        elif credentials_path.exists():
            credentials_path.unlink()

    def _load_state(self) -> None:
        if not self.state_path.exists():
            return
        try:
            payload = json.loads(self.state_path.read_text())
        except Exception:
            return
        self.selected_provider_ids = [str(item) for item in payload.get("selected_provider_ids", [])]
        self.active_provider_id = payload.get("active_provider_id") or None
        self.current_step = str(payload.get("current_step", self.current_step))
        self.continue_after_first_success = bool(payload.get("continue_after_first_success", True))
        saved_setups = payload.get("provider_setups", {})
        if isinstance(saved_setups, dict):
            for provider_id, setup_payload in saved_setups.items():
                if provider_id not in self.provider_setups or not isinstance(setup_payload, dict):
                    continue
                setup = self.provider_setups[provider_id]
                setup.status = str(setup_payload.get("status", setup.status))
                setup.severity = str(setup_payload.get("severity", setup.severity))
                setup.readiness_detail = str(setup_payload.get("readiness_detail", setup.readiness_detail))
                setup.api_key_value = str(setup_payload.get("api_key_value", setup.api_key_value))
                self._persist_provider_entry(setup)

    def _save_state(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "selected_provider_ids": self.selected_provider_ids,
            "active_provider_id": self.active_provider_id,
            "current_step": self.current_step,
            "continue_after_first_success": self.continue_after_first_success,
            "provider_setups": {
                provider_id: {
                    "status": setup.status,
                    "severity": setup.severity,
                    "readiness_detail": setup.readiness_detail,
                    "api_key_value": setup.api_key_value,
                }
                for provider_id, setup in self.provider_setups.items()
            },
        }
        self.state_path.write_text(json.dumps(payload, indent=2) + "\n")


def build_onboarding_screen_view_model(base_path: Path) -> OnboardingScreenViewModel:
    return OnboardingScreenViewModel(state_path=base_path / "var" / "onboarding_state.json")
