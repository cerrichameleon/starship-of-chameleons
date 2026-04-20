from __future__ import annotations

import json
from pathlib import Path

from starship_protocol.captain_chat import build_captain_chat_session


MISSION_STATEMENT = (
    "You are the Captain of a Starship of Chameleons. "
    "You are the singular public-facing command mind of the ship. "
    "The user speaks to you, and you coordinate the rest of the ship. "
    "If you understand who you are and what your protocol is, say yes and state your case clearly."
)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    session = build_captain_chat_session(root, provider="openclaw")

    if session.craft.captain.brain is not None and hasattr(session.craft.captain.brain, "mission_statement"):
        session.craft.captain.brain.mission_statement = MISSION_STATEMENT

    transcript: list[dict[str, str]] = []

    captain_opening = session.talk_to_captain(
        "Read your mission statement, acknowledge that you understand your role, and introduce yourself as Captain."
    )
    transcript.append({"role": "captain", "text": captain_opening})

    welcome = "Welcome aboard, Captain. Confirm bridge readiness in one sentence."
    transcript.append({"role": "system", "text": welcome})
    captain_reply = session.talk_to_captain(welcome)
    transcript.append({"role": "captain", "text": captain_reply})

    log_path = root / "var" / "captain_handshake_log.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(transcript, indent=2), encoding="utf-8")

    print(json.dumps({"log_path": str(log_path), "transcript": transcript}, indent=2))


if __name__ == "__main__":
    main()
