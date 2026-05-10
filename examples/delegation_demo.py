from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from starship_protocol.engineering import ChiefEngineer
from starship_protocol.providers import OpenClawProvider
from starship_protocol.roles import Captain, Specialist
from starship_protocol.starship import Starship


def main() -> None:
    provider = OpenClawProvider()

    captain = Captain(name="Captain Ultra")
    engineer = ChiefEngineer(name="Chief Engineer", reports_to=captain.chameleon_id)
    coder = Specialist(name="Chief Coder", focus_area="software", reports_to=captain.chameleon_id)

    engineer.outfit_with_provider(
        captain,
        provider,
        model_id="gpt-5.4",
        credentials_ref="env:OPENAI_API_KEY",
        capabilities=["command", "planning", "bridge-comms"],
    )
    engineer.outfit_with_provider(
        coder,
        provider,
        model_id="gpt-5.4",
        credentials_ref="env:OPENAI_API_KEY",
        capabilities=["coding", "analysis"],
    )

    ship = Starship(name="Starship of Chameleons", ship_class="light-craft", captain=captain)
    ship.register_crew(coder)

    captain_prompt = "Chief Coder, tell me in one sentence how you would approach building a small Python CLI bridge."
    captain_reply = captain.think(
        mission="delegate first specialist task",
        channel_status="bridge delegation ready",
        user_message=f"You are about to delegate this request: {captain_prompt}",
    )
    delegated = ship.delegate(
        focus_area="software",
        title="cli-bridge",
        description=captain_prompt,
    )

    print(
        json.dumps(
            {
                "captain_reply": captain_reply,
                "delegation": delegated,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
