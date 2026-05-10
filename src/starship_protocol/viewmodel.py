from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import parse_qs

from .monitoring import ShipMonitor
from .runtime import StarshipRuntime


@dataclass
class ChatMessageViewData:
    role: str
    text: str


@dataclass
class CrewMonitorViewData:
    name: str
    ship_id: str
    role_name: str
    group_tags: list[str] = field(default_factory=list)
    has_brain: bool = False
    status: str = "IDLE"
    working_memory_events: int = 0
    activity_level: int = 0


@dataclass
class ChatTabViewModel:
    title: str = "Starship of Chameleons"
    subtitle: str = "Captain chat interface, user and Captain only."
    placeholder_text: str = "Send an order to the Captain..."
    send_button_text: str = "Send"
    startup_manifest_lines: list[str] = field(default_factory=list)
    messages: list[ChatMessageViewData] = field(default_factory=list)


@dataclass
class MonitorTabViewModel:
    tick_count: int = 0
    last_tick_at: str | None = None
    crew_entries: list[CrewMonitorViewData] = field(default_factory=list)


@dataclass
class CaptainConsoleScreenViewModel:
    runtime: StarshipRuntime
    active_tab: str = "chat"
    chat_tab: ChatTabViewModel = field(default_factory=ChatTabViewModel)
    monitor_tab: MonitorTabViewModel = field(default_factory=MonitorTabViewModel)

    @property
    def messages(self) -> list[ChatMessageViewData]:
        return self.chat_tab.messages

    def refresh(self) -> None:
        self.chat_tab.startup_manifest_lines = self.runtime.captain_console.get_startup_manifest_lines()
        self.chat_tab.messages = [
            ChatMessageViewData(role=turn.role, text=turn.text)
            for turn in self.runtime.captain_chat_session.history
        ]
        monitor_snapshot = ShipMonitor(self.runtime).capture_snapshot()
        self.monitor_tab.tick_count = monitor_snapshot.tick_count
        self.monitor_tab.last_tick_at = monitor_snapshot.last_tick_at
        self.monitor_tab.crew_entries = [
            CrewMonitorViewData(
                name=entry.name,
                ship_id=entry.ship_id,
                role_name=entry.role_name,
                group_tags=list(entry.group_tags),
                has_brain=entry.has_brain,
                status=entry.status,
                working_memory_events=entry.working_memory_events,
                activity_level=entry.activity_level,
            )
            for entry in monitor_snapshot.crew_entries
        ]

    def submit_user_message(self, raw_form_body: str) -> None:
        parsed_form = parse_qs(raw_form_body, keep_blank_values=True)
        self.active_tab = parsed_form.get("tab", [self.active_tab])[0] or "chat"
        message_text = parsed_form.get("message", [""])[0].strip()
        if not message_text:
            self.refresh()
            return
        self.runtime.captain_console.submit_chat_message(message_text)
        self.refresh()


def build_captain_console_screen_view_model(runtime: StarshipRuntime) -> CaptainConsoleScreenViewModel:
    view_model = CaptainConsoleScreenViewModel(runtime=runtime)
    view_model.refresh()
    return view_model


def build_captain_chat_view_model(runtime: StarshipRuntime) -> CaptainConsoleScreenViewModel:
    return build_captain_console_screen_view_model(runtime)
