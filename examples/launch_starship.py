from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from starship_protocol.runtime import build_runtime


def run_cli() -> None:
    runtime = build_runtime()
    summary = runtime.captain_chat_session.summarize_state()
    print(f"{summary['ship']} is online.")
    print(f"Captain: {summary['captain']}")
    print("Type your orders. Type 'exit' to leave the bridge.")

    while True:
        user_message = input("you> ").strip()
        if not user_message:
            continue
        if user_message.lower() in {"exit", "quit"}:
            print("bridge> standing down.")
            break
        reply = runtime.captain_chat_session.talk_to_captain(user_message)
        print(f"captain> {reply}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch the Starship of Chameleons.")
    parser.add_argument("--mode", choices=["cli"], default="cli")
    args = parser.parse_args()

    if args.mode == "cli":
        run_cli()


if __name__ == "__main__":
    main()
