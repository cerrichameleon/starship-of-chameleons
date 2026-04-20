from __future__ import annotations

import argparse
import json
from pathlib import Path

from starship_protocol.xwing_protocol import ProtocolError, build_default_xwing


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Starship X-Wing Captain/Uhura demo")
    parser.add_argument("command", choices=["open", "captain", "diagnose", "close", "demo"])
    parser.add_argument("--target", default="captain-bridge", help="Approved target for Uhura to open")
    parser.add_argument("--prompt", default="Give me a concise bridge update.", help="Prompt for the Captain brain")
    parser.add_argument("--base-path", default=".", help="Project root for audit files")
    parser.add_argument("--provider", default="openclaw", choices=["openclaw", "mock"], help="Captain brain provider adapter")
    args = parser.parse_args()

    craft = build_default_xwing(Path(args.base_path).resolve(), provider=args.provider)

    if args.command == "open":
        try:
            print(craft.open_channel(args.target))
        except ProtocolError as exc:
            print(f"Uhura: {exc}")
        return

    if args.command == "captain":
        if not craft.active_channel:
            try:
                craft.open_channel(args.target)
            except ProtocolError:
                pass
        print(craft.captain_speak(args.prompt))
        return

    if args.command == "diagnose":
        if not craft.active_channel:
            try:
                craft.open_channel(args.target)
            except ProtocolError:
                pass
        print(json.dumps(craft.diagnose_channel(), indent=2))
        return

    if args.command == "close":
        if not craft.active_channel:
            try:
                craft.open_channel(args.target)
            except ProtocolError:
                pass
        print(craft.close_channel())
        return

    if args.command == "demo":
        try:
            print(craft.open_channel(args.target))
        except ProtocolError as exc:
            print(f"Uhura: {exc}")
        print()
        print(craft.captain_speak(args.prompt))
        print()
        print(json.dumps(craft.diagnose_channel(), indent=2))
        print()
        print(craft.close_channel())
        return


if __name__ == "__main__":
    main()
