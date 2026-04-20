from __future__ import annotations

import argparse
import json
from pathlib import Path

from starship_protocol.captain_chat import build_captain_chat_session


def main() -> None:
    parser = argparse.ArgumentParser(description="Talk directly to the Starship Captain")
    parser.add_argument("message", nargs="?", help="One-shot message for the Captain")
    parser.add_argument("--provider", default="mock", choices=["openclaw", "mock"], help="Captain brain provider")
    parser.add_argument("--base-path", default=".", help="Project root for state files")
    parser.add_argument("--status", action="store_true", help="Show Captain chat session status")
    parser.add_argument("--interactive", action="store_true", help="Start an interactive Captain shell")
    args = parser.parse_args()

    session = build_captain_chat_session(Path(args.base_path).resolve(), provider=args.provider)

    if args.status:
        print(json.dumps(session.summarize_state(), indent=2))
        return

    if args.interactive:
        print("Captain bridge open. Type 'exit' to leave.")
        while True:
            try:
                line = input("you> ").strip()
            except EOFError:
                break
            if not line or line.lower() in {"exit", "quit"}:
                break
            print(f"captain> {session.talk_to_captain(line)}")
        return

    if not args.message:
        parser.error("message required unless using --status or --interactive")

    print(session.talk_to_captain(args.message))


if __name__ == "__main__":
    main()
