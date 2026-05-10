from __future__ import annotations

import html
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .runtime import build_runtime
from .viewmodel import CaptainChatViewModel, build_captain_chat_view_model


def render_page(view_model: CaptainChatViewModel) -> str:
    rendered_messages = "\n".join(
        f"<div class='message {html.escape(item.role)}'><div class='speaker'>{html.escape(item.role)}</div><div class='text'>{html.escape(item.text)}</div></div>"
        for item in view_model.messages
    )
    return f"""
<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>Starship of Chameleons</title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #0b1020; color: #e6ecff; margin: 0; }}
    .shell {{ max-width: 900px; margin: 0 auto; padding: 24px; }}
    h1 {{ margin-bottom: 8px; }}
    .subtitle {{ color: #9fb0e0; margin-bottom: 20px; }}
    .chat {{ background: #111833; border: 1px solid #2a3768; border-radius: 12px; padding: 16px; min-height: 420px; max-height: 60vh; overflow-y: auto; }}
    .message {{ padding: 12px; margin-bottom: 12px; border-radius: 10px; }}
    .message.user {{ background: #1c2855; }}
    .message.captain {{ background: #17243d; }}
    .speaker {{ font-size: 12px; text-transform: uppercase; color: #8fa4e8; margin-bottom: 6px; }}
    .text {{ white-space: pre-wrap; line-height: 1.4; }}
    form {{ display: flex; gap: 12px; margin-top: 16px; }}
    textarea {{ flex: 1; min-height: 90px; border-radius: 10px; border: 1px solid #2a3768; background: #0f1730; color: #e6ecff; padding: 12px; }}
    button {{ border: 0; border-radius: 10px; background: #5d7cff; color: white; padding: 0 18px; font-weight: bold; cursor: pointer; }}
    button:hover {{ background: #7690ff; }}
  </style>
</head>
<body>
  <div class='shell'>
    <h1>{html.escape(view_model.title)}</h1>
    <div class='subtitle'>{html.escape(view_model.subtitle)}</div>
    <div class='chat'>{rendered_messages}</div>
    <form method='post' action='/chat'>
      <textarea name='message' placeholder='{html.escape(view_model.placeholder_text)}'></textarea>
      <button type='submit'>{html.escape(view_model.send_button_text)}</button>
    </form>
  </div>
</body>
</html>
"""


class StarshipWebHandler(BaseHTTPRequestHandler):
    view_model = None

    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        self.view_model.refresh()
        body = render_page(self.view_model).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/chat":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        content_length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(content_length).decode("utf-8")
        self.view_model.submit_user_message(payload)
        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header("Location", "/")
        self.end_headers()

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return


def launch_web_ui(host: str = "127.0.0.1", port: int = 8765, base_path: Path | None = None) -> None:
    runtime = build_runtime(base_path=base_path)
    StarshipWebHandler.view_model = build_captain_chat_view_model(runtime)
    server = ThreadingHTTPServer((host, port), StarshipWebHandler)
    print(json.dumps({"status": "online", "url": f"http://{host}:{port}", "captain": runtime.starship.captain.name}))
    server.serve_forever()
