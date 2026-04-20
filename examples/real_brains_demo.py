from __future__ import annotations

from starship_protocol.engineering import ChiefEngineer
from starship_protocol.providers import OpenClawProvider
from starship_protocol.roles import Captain, Specialist


def main() -> None:
    provider = OpenClawProvider()

    captain = Captain(name="Captain Ultra")
    engineer = ChiefEngineer(name="Chief Engineer", reports_to=captain.chameleon_id)
    coder = Specialist(name="Chief Coder", focus_area="software", reports_to=captain.chameleon_id)

    engineer.outfit_with_provider(
        captain,
        provider,
        model_id="gpt-5.4",
        credentials_ref="auth-profile:openai-codex:mattcleere@gmail.com",
        capabilities=["command", "planning", "bridge-comms"],
    )
    engineer.outfit_with_provider(
        coder,
        provider,
        model_id="gpt-5.4",
        credentials_ref="auth-profile:openai-codex:mattcleere@gmail.com",
        capabilities=["coding", "analysis"],
    )

    captain_reply = captain.think(
        mission="demonstrate real brains across chameleons",
        channel_status="captain bridge open",
        user_message="Give me a one-sentence bridge update.",
    )
    coder_reply = coder.think(
        mission="demonstrate real brains across chameleons",
        channel_status="coding bay ready",
        user_message="In one sentence, say what you are responsible for.",
    )

    print({
        "captain_has_brain": captain.has_brain(),
        "coder_has_brain": coder.has_brain(),
        "captain_brain_profile": captain.brain_profile,
        "coder_brain_profile": coder.brain_profile,
        "captain_reply": captain_reply,
        "coder_reply": coder_reply,
    })


if __name__ == "__main__":
    main()
