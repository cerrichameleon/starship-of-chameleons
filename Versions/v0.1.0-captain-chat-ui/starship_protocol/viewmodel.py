from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import parse_qs

from .runtime import StarshipRuntime


@dataclass
class ChatMessageViewData:
    role: str
    text: str


@dataclass
class CaptainChatViewModel:
    runtime: StarshipRuntime
    title: str = "Starship of Chameleons"
    subtitle: str = "Captain chat interface, user and Captain only."
    placeholder_text: str = "Send an order to the Captain..."
    send_button_text: str = "Send"
    messages: list[ChatMessageViewData] = field(default_factory=list)

    def refresh(self) -> None:
        self.messages = [
            ChatMessageViewData(role=turn.role, text=turn.text)
            for turn in self.runtime.captain_chat_session.history
        ]

    def submit_user_message(self, raw_form_body: str) -> None:
        parsed_form = parse_qs(raw_form_body, keep_blank_values=True)
        message_text = parsed_form.get("message", [""])[0].strip()
        if not message_text:
            return
        self.runtime.captain_console.submit_chat_message(message_text)
        self.refresh()


def build_captain_chat_view_model(runtime: StarshipRuntime) -> CaptainChatViewModel:
    view_model = CaptainChatViewModel(runtime=runtime)
    view_model.refresh()
    return view_model
