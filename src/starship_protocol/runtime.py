from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .activity_log import ActivityLogStore
from .brain_selection import LaunchPolicy, select_brain_for_launch
from .captain_chat import CaptainConversationSession
from .captain_console import CaptainConsole
from .crew_factory import CrewFactory
from .drydock import DryDockController
from .comms import Uhura
from .engineering import ChiefEngineer
from .internal_comms import InternalCommunicationsHub
from .providers import OpenClawProvider
from .roles import Captain
from .ship_clock import ShipClock
from .starship import Starship
from .usage_tracker import EstimatedUsageTracker
from .work_tracker import WorkTracker


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
    crew_factory: CrewFactory
    internal_comms: InternalCommunicationsHub
    ship_clock: ShipClock
    work_tracker: WorkTracker
    drydock_controller: DryDockController
    activity_log_store: ActivityLogStore
    usage_tracker: EstimatedUsageTracker
    uhura: Uhura


def build_runtime(base_path: Path | None = None, launch_policy: LaunchPolicy | None = None) -> StarshipRuntime:
    root = (base_path or Path.cwd()).resolve()
    selection = select_brain_for_launch(policy=launch_policy)
    if selection.provider_id == "unavailable":
        raise RuntimeError(
            "No real brain provider is currently available. Expected cascade: Codex, then OpenAI API, then Gemini API."
        )

    provider = OpenClawProvider(provider_id=selection.provider_id)

    crew_factory = CrewFactory()
    internal_comms = InternalCommunicationsHub()
    ship_clock = ShipClock()
    work_tracker = WorkTracker()
    activity_log_store = ActivityLogStore(root / "var" / "activity_logs")
    usage_tracker = EstimatedUsageTracker()
    captain = Captain(name="Captain")
    chief_engineer = ChiefEngineer(name="Chief Engineer", reports_to=captain.chameleon_id)
    uhura = crew_factory.create_comms_officer(
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
            model_id=selection.model_label if selection.model_label != "gateway-managed" else "gpt-5.4",
            credentials_ref=selection.credentials_ref,
            capabilities=capabilities,
            selected_provider_order=list(launch_policy.provider_order) if launch_policy else [],
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
    runtime = StarshipRuntime(
        starship=starship,
        captain_chat_session=session,
        captain_console=console,
        crew_factory=crew_factory,
        internal_comms=internal_comms,
        ship_clock=ship_clock,
        work_tracker=work_tracker,
        drydock_controller=None,  # type: ignore[arg-type]
        activity_log_store=activity_log_store,
        usage_tracker=usage_tracker,
        uhura=uhura,
    )
    runtime.drydock_controller = DryDockController(runtime)
    console.runtime = runtime
    return runtime
