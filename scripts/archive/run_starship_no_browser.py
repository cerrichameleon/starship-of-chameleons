from __future__ import annotations

import json
import os
import socket
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from starship_protocol.brain_selection import select_brain_for_launch
from starship_protocol.onboarding_ui import build_onboarding_screen_view_model
from starship_protocol.web_ui import launch_web_ui

DEFAULT_PORT = 8765


def port_is_available(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as candidate_socket:
        candidate_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            candidate_socket.bind((host, port))
        except OSError:
            return False
    return True


def choose_port(start_port: int = DEFAULT_PORT) -> int:
    for candidate_port in range(start_port, start_port + 20):
        if port_is_available(candidate_port):
            return candidate_port
    raise RuntimeError("No available port found in the default Starship UI range")


def main() -> None:
    project_root = PROJECT_ROOT
    onboarding_view_model = build_onboarding_screen_view_model(project_root)
    launch_policy = onboarding_view_model.get_launch_policy()
    selection = select_brain_for_launch(policy=launch_policy)
    if selection.provider_id == "unavailable":
        raise RuntimeError("No real brain provider was available for launch.")
    os.environ["STARSHIP_SELECTED_PROVIDER"] = selection.provider_id
    os.environ["STARSHIP_SELECTED_MODEL"] = selection.model_label
    os.environ["STARSHIP_SELECTED_ACCESS_PATH"] = selection.access_path
    os.environ["STARSHIP_SELECTED_PROVIDER_ORDER"] = ",".join(launch_policy.provider_order)
    port = choose_port()
    url = f"http://127.0.0.1:{port}"
    onboarding_url = f"{url}/onboarding"
    print(
        json.dumps(
            {
                "status": "launching",
                "mode": "host-ui-no-browser-opener",
                "url": url,
                "onboarding_url": onboarding_url,
                "project_root": str(project_root),
                "brain_provider": selection.provider_label,
                "brain_model": selection.model_label,
                "brain_access_path": selection.access_path,
                "selected_provider_order": launch_policy.provider_order,
                "using_tokens": selection.using_tokens,
                "launch_note": selection.launch_note,
                "attempt_log": selection.attempt_log,
            }
        ),
        flush=True,
    )
    launch_web_ui(host="127.0.0.1", port=port, base_path=project_root)


if __name__ == "__main__":
    main()
