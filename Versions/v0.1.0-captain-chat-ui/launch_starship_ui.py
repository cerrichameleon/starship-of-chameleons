from __future__ import annotations

import argparse
from pathlib import Path

from starship_protocol.web_ui import launch_web_ui


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch the Starship of Chameleons web UI.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--base-path", default=str(Path.cwd()))
    args = parser.parse_args()
    launch_web_ui(host=args.host, port=args.port, base_path=Path(args.base_path))


if __name__ == "__main__":
    main()
