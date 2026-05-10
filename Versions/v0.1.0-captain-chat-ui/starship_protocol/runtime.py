from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .captain_chat import CaptainConversationSession
from .captain_console import CaptainConsole
from .comms import Uhura
from .engineering import ChiefEngineer
from .providers import OpenClawProvider
from .roles import Captain
from .starship import Starship


class RuntimeCaptainBridge:
    def __init__(self, starship: Starship, uhura: Uhura, mission: str) -> None:
        self.name = starship.name
        self.captain = starship.captain
        self.uhura = uhura
        self.mission = mission
        self.active_channel = uhura.get_active_channel()

    def open_channel(self, target: str) -> str:
        self.active_channel = self.uhura.open_channel(target)
        return self.uhura.notify_captain_channel_open(self.active_channel)

    def captain_speak(self, prompt: str) -> str:
        active_channel = self.uhura.get_active_channel()
        channel_status = (
            f"channel {active_channel.channel_id} open to {active_channel.target}"
            if active_channel
            else "no active channel"
        )
        return self.captain.think(
            mission=self.mission,
            channel_status=channel_status,
            user_message=prompt,
        )


@dataclass
class StarshipRuntime:
    starship: Starship
    captain_chat_session: CaptainConversationSession
    captain_console: CaptainConsole
    uhura: Uhura


def build_runtime(base_path: Path | None = None) -> StarshipRuntime:
    root = (base_path or Path.cwd()).resolve()
    provider = OpenClawProvider()

    captain = Captain(name="Captain")
    chief_engineer = ChiefEngineer(name="Chief Engineer", reports_to=captain.chameleon_id)
    uhura = Uhura(
        name="Uhura",
        allowed_targets={"user-dm", "captain-bridge", "mission-control"},
        audit_path=root / "var" / "uhura_audit.log",
        state_path=root / "var" / "uhura_state.json",
        reports_to=captain.chameleon_id,
    )

    starship = Starship(
        name="Starship of Chameleons",
        ship_class="adaptive-command",
        captain=captain,
        chief_engineer=chief_engineer,
    )
    starship.register_crew(uhura, role_name="comms-officer", ship_id_prefix="comms-officer", group_tags=["comms"])

    for crew_member, capabilities in [
        (captain, ["command", "crew-design", "delegation", "approval"]),
        (chief_engineer, ["brain-outfitting", "provider-selection", "technical-review"]),
        (uhura, ["communications", "channel-security", "captain-routing"]),
    ]:
        chief_engineer.outfit_with_provider(
            crew_member,
            provider,
            model_id="gpt-5.4",
            credentials_ref="env:OPENAI_API_KEY",
            capabilities=capabilities,
        )

    runtime_bridge = RuntimeCaptainBridge(
        starship=starship,
        uhura=uhura,
        mission="Operate as a real Starship runtime.",
    )
    session = CaptainConversationSession(
        craft=runtime_bridge,
        state_path=root / "var" / "captain_chat_state.json",
    )
    console = CaptainConsole(runtime=None)  # type: ignore[arg-type]
    runtime = StarshipRuntime(starship=starship, captain_chat_session=session, captain_console=console, uhura=uhura)
    console.runtime = runtime
    return runtime
