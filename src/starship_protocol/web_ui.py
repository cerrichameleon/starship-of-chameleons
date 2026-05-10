from __future__ import annotations

import html
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .onboarding_ui import OnboardingScreenViewModel, build_onboarding_screen_view_model
from .runtime import build_runtime
from .viewmodel import CaptainConsoleScreenViewModel, build_captain_console_screen_view_model


def render_onboarding_page(view_model: OnboardingScreenViewModel) -> str:
    readiness_overview = "".join(
        "<tr>"
        f"<td>{html.escape(setup.label)}</td>"
        f"<td><span class='status-dot status-dot-{html.escape(setup.severity)}'></span>{html.escape(setup.status)}</td>"
        f"<td>{html.escape(setup.readiness_detail)}</td>"
        "</tr>"
        for setup in view_model.provider_setups.values()
    )
    if view_model.current_step == "select":
        order_items = "".join(
            f"<li class='order-item' draggable='true' data-provider-id='{html.escape(option.provider_id)}'>{html.escape(option.label)}</li>"
            for option in view_model.provider_options
        )
        option_blocks = "".join(
            "<label class='provider-option'>"
            f"<input type='checkbox' name='provider' value='{html.escape(option.provider_id)}' {'checked' if option.provider_id in view_model.selected_provider_ids else ''}>"
            f"<strong>{html.escape(option.label)}</strong>"
            f"<div class='provider-description'>{html.escape(option.description)}</div>"
            "</label>"
            for option in view_model.provider_options
        )
        continue_mode = "first-success" if not view_model.continue_after_first_success else "all"
        panel_html = (
            "<h2>Choose your provider(s)</h2>"
            "<p>Select the providers you want, then choose their order. Drag the order list to put your preferred provider on top.</p>"
            "<form method='post' action='/onboarding/select' id='provider-selection-form'>"
            f"{option_blocks}"
            "<h3>Please choose your order as well</h3>"
            f"<ol id='provider-order-list'>{order_items}</ol>"
            "<input type='hidden' name='provider_order' id='provider_order_input'>"
            "<label class='continue-mode'><input type='radio' name='continue_mode' value='all'"
            + (" checked" if continue_mode == "all" else "")
            + "> Continue hooking up the other selected providers now</label>"
            "<label class='continue-mode'><input type='radio' name='continue_mode' value='first-success'"
            + (" checked" if continue_mode == "first-success" else "")
            + "> Stop after the first successful connection and use that as the brain for now</label>"
            "<button type='submit'>Continue</button>"
            "</form>"
        )
    elif view_model.current_step == "setup" and view_model.active_provider_id:
        setup = view_model.provider_setups[view_model.active_provider_id]
        help_blocks = "".join(
            "<details class='help-block' open>"
            f"<summary>{html.escape(key.replace('-', ' '))}</summary>"
            f"<pre>{html.escape(text)}</pre>"
            "</details>"
            for key, text in setup.help_sections.items()
        )
        if setup.needs_api_key:
            input_block = (
                "<label>Enter your API key here"
                f"<input type='text' name='api_key' value='{html.escape(setup.api_key_value)}'>"
                "</label>"
            )
        else:
            input_block = (
                "<div class='oauth-box'>"
                "This path requires a one-time human login. Follow the instructions below, then click Continue after you finish the login flow."
                "</div>"
            )
        panel_html = (
            f"<h2>Set up {html.escape(setup.label)}</h2>"
            f"<div class='status-line status-line-{html.escape(setup.severity)}'>Status: {html.escape(setup.status)}</div>"
            f"<div class='readiness-detail'>{html.escape(setup.readiness_detail)}</div>"
            "<form method='post' action='/onboarding/setup'>"
            f"<input type='hidden' name='provider_id' value='{html.escape(setup.provider_id)}'>"
            f"<input type='hidden' name='continue_mode' value={'all' if view_model.continue_after_first_success else 'first-success'}>"
            f"{input_block}"
            f"{help_blocks}"
            "<button type='submit'>Continue</button>"
            "</form>"
        )
    else:
        status_rows = "".join(
            "<tr>"
            f"<td>{html.escape(setup.label)}</td>"
            f"<td><span class='status-dot status-dot-{html.escape(setup.severity)}'></span>{html.escape(setup.status)}</td>"
            f"<td>{html.escape(setup.readiness_detail)}</td>"
            "</tr>"
            for provider_id, setup in view_model.provider_setups.items()
            if provider_id in view_model.selected_provider_ids
        )
        selected_order_text = ", ".join(
            view_model.provider_setups[provider_id].label
            for provider_id in view_model.selected_provider_ids
            if provider_id in view_model.provider_setups
        ) or "No provider order selected yet."
        panel_html = (
            "<h2>Provider Monitor</h2>"
            "<p>At least one selected provider is ready. You can open a fresh Captain chat now, go back and finish the rest of your selected hookups, or reset onboarding and start over cleanly.</p>"
            f"<div class='readiness-detail'><strong>Captain launch order:</strong> {html.escape(selected_order_text)}</div>"
            "<div class='readiness-detail'>Starship will use the first ready provider in that order when you open the Captain chat.</div>"
            "<table><thead><tr><th>Provider</th><th>Status</th><th>Readiness detail</th></tr></thead>"
            f"<tbody>{status_rows}</tbody></table>"
            "<a class='launch-link' href='/?tab=chat&fresh=1'>Start talking to the Captain</a>"
            "<a class='secondary-link' href='/onboarding'>Adjust providers</a>"
            "<form method='post' action='/onboarding/reset' class='inline-form'><button class='secondary-button' type='submit'>Start onboarding over</button></form>"
        )
    return f"""
<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>Starship Onboarding</title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #0b1020; color: #e6ecff; margin: 0; }}
    .shell {{ max-width: 960px; margin: 0 auto; padding: 24px; }}
    .panel {{ background: #111833; border: 1px solid #2a3768; border-radius: 12px; padding: 20px; }}
    .provider-option {{ display: block; background: #0f1730; border: 1px solid #2a3768; border-radius: 10px; padding: 12px; margin-bottom: 12px; }}
    .provider-description {{ color: #9fb0e0; margin-top: 4px; }}
    .help-block {{ margin-top: 12px; background: #0f1730; border-radius: 8px; padding: 8px; }}
    .help-block pre {{ white-space: pre-wrap; color: #d7e2ff; }}
    .status-line {{ margin-bottom: 8px; color: #9fb0e0; font-weight: bold; }}
    .status-line-green {{ color: #7ee787; }}
    .status-line-yellow {{ color: #f2cc60; }}
    .status-line-red {{ color: #ff7b72; }}
    .readiness-detail {{ margin-bottom: 12px; color: #c8d4ff; }}
    .oauth-box {{ background: #0f1730; border: 1px solid #2a3768; border-radius: 10px; padding: 12px; margin-bottom: 12px; }}
    .overview {{ margin-top: 18px; background: #0f1730; border: 1px solid #2a3768; border-radius: 10px; padding: 16px; }}
    .continue-mode {{ display: block; margin-top: 12px; color: #d7e2ff; }}
    .order-item {{ background: #0f1730; border: 1px solid #2a3768; border-radius: 8px; padding: 10px; margin-bottom: 8px; cursor: grab; }}
    .order-item.dragging {{ opacity: 0.55; }}
    input[type='text'] {{ width: 100%; margin-top: 8px; padding: 10px; border-radius: 8px; border: 1px solid #2a3768; background: #0f1730; color: #e6ecff; }}
    button, .launch-link, .secondary-link, .secondary-button {{ display: inline-block; margin-top: 16px; margin-right: 12px; border: 0; border-radius: 10px; background: #5d7cff; color: white; padding: 10px 16px; font-weight: bold; cursor: pointer; text-decoration: none; }}
    .secondary-link, .secondary-button {{ background: #243152; }}
    .inline-form {{ display: inline; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
    th, td {{ text-align: left; padding: 10px; border-bottom: 1px solid #25345f; vertical-align: top; }}
    .status-dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 999px; margin-right: 8px; }}
    .status-dot-green {{ background: #2ecc71; }}
    .status-dot-yellow {{ background: #f1c40f; }}
    .status-dot-red {{ background: #ff5f56; }}
  </style>
</head>
<body>
  <div class='shell'>
    <div class='panel'>
      {panel_html}
      <div class='overview'>
        <h3>Current readiness snapshot</h3>
        <table><thead><tr><th>Provider</th><th>Status</th><th>Detail</th></tr></thead><tbody>{readiness_overview}</tbody></table>
      </div>
    </div>
  </div>
  <script>
    const orderList = document.getElementById('provider-order-list');
    const orderInput = document.getElementById('provider_order_input');
    if (orderList && orderInput) {{
      const syncOrder = () => {{
        orderInput.value = Array.from(orderList.querySelectorAll('.order-item')).map(item => item.dataset.providerId).join(',');
      }};
      let dragged = null;
      orderList.querySelectorAll('.order-item').forEach(item => {{
        item.addEventListener('dragstart', () => {{ dragged = item; item.classList.add('dragging'); }});
        item.addEventListener('dragend', () => {{ item.classList.remove('dragging'); syncOrder(); }});
        item.addEventListener('dragover', event => {{
          event.preventDefault();
          if (!dragged || dragged === item) return;
          const rect = item.getBoundingClientRect();
          const after = (event.clientY - rect.top) > rect.height / 2;
          if (after) {{ item.after(dragged); }} else {{ item.before(dragged); }}
        }});
      }});
      syncOrder();
    }}
  </script>
</body>
</html>
"""


def render_page(view_model: CaptainConsoleScreenViewModel) -> str:
    rendered_manifest = "".join(
        f"<li>{html.escape(line)}</li>" for line in view_model.chat_tab.startup_manifest_lines
    )
    rendered_messages = "\n".join(
        f"<div class='message {html.escape(item.role)}'><div class='speaker'>{html.escape(item.role)}</div><div class='text'>{html.escape(item.text)}</div></div>"
        for item in view_model.chat_tab.messages
    )
    rendered_monitor_rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(item.name)}</td>"
        f"<td>{html.escape(item.ship_id)}</td>"
        f"<td>{html.escape(item.role_name)}</td>"
        f"<td><span class='status-light {html.escape(item.status.lower())}'></span>{html.escape(item.status.lower())}</td>"
        f"<td>{'yes' if item.has_brain else 'no'}</td>"
        f"<td>{item.working_memory_events}</td>"
        f"<td>{item.activity_level}%</td>"
        "</tr>"
        for item in view_model.monitor_tab.crew_entries
    )
    active_chat_class = "active" if view_model.active_tab == "chat" else ""
    active_monitor_class = "active" if view_model.active_tab == "monitor" else ""
    if view_model.active_tab == "chat":
        panel_html = (
            f"<div class='manifest'><div class='manifest-title'>current outfit</div><ul>{rendered_manifest}</ul></div>"
            f"<div class='chat' id='chat-log'>{rendered_messages}</div>"
            f"<form method='post' action='/chat'>"
            f"<input type='hidden' name='tab' value='chat'>"
            f"<textarea name='message' placeholder='{html.escape(view_model.chat_tab.placeholder_text)}'></textarea>"
            f"<button type='submit'>{html.escape(view_model.chat_tab.send_button_text)}</button>"
            f"</form>"
        )
    else:
        panel_html = (
            f"<div class='monitor-meta'>tick: {view_model.monitor_tab.tick_count} | last tick: {html.escape(view_model.monitor_tab.last_tick_at or 'not yet')}</div>"
            f"<table>"
            f"<thead><tr><th>name</th><th>ship id</th><th>designation</th><th>status</th><th>brain</th><th>events</th><th>activity</th></tr></thead>"
            f"<tbody>{rendered_monitor_rows}</tbody>"
            f"</table>"
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
    .tabs {{ display: flex; gap: 8px; margin-bottom: 16px; }}
    .tab {{ padding: 10px 14px; border-radius: 10px; background: #17243d; color: #cdd8ff; text-decoration: none; border: 1px solid #2a3768; }}
    .tab.active {{ background: #5d7cff; color: white; }}
    .quick-onboarding {{ margin-left: auto; }}
    .panel {{ background: #111833; border: 1px solid #2a3768; border-radius: 12px; padding: 16px; }}
    .manifest {{ background: #0f1730; border: 1px solid #2a3768; border-radius: 10px; padding: 12px; margin-bottom: 16px; }}
    .manifest-title {{ color: #8fa4e8; text-transform: uppercase; font-size: 12px; margin-bottom: 8px; }}
    .manifest ul {{ margin: 0; padding-left: 18px; }}
    .manifest li {{ margin-bottom: 4px; color: #d7e2ff; }}
    .chat {{ min-height: 420px; max-height: 60vh; overflow-y: auto; }}
    .message {{ padding: 12px; margin-bottom: 12px; border-radius: 10px; }}
    .message.user {{ background: #1c2855; }}
    .message.captain {{ background: #17243d; }}
    .speaker {{ font-size: 12px; text-transform: uppercase; color: #8fa4e8; margin-bottom: 6px; }}
    .text {{ white-space: pre-wrap; line-height: 1.4; }}
    form {{ display: flex; gap: 12px; margin-top: 16px; }}
    textarea {{ flex: 1; min-height: 90px; border-radius: 10px; border: 1px solid #2a3768; background: #0f1730; color: #e6ecff; padding: 12px; }}
    button {{ border: 0; border-radius: 10px; background: #5d7cff; color: white; padding: 0 18px; font-weight: bold; cursor: pointer; }}
    button:hover {{ background: #7690ff; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ text-align: left; padding: 10px; border-bottom: 1px solid #25345f; }}
    .monitor-meta {{ color: #9fb0e0; margin-bottom: 16px; }}
    .status-light {{ display: inline-block; width: 10px; height: 10px; border-radius: 999px; margin-right: 8px; }}
    .status-light.idle {{ background: #ff5f56; }}
    .status-light.active {{ background: #2ecc71; }}
    .status-light.paused {{ background: #f1c40f; }}
    .status-light.error {{ background: #ff5f56; }}
  </style>
</head>
<body>
  <div class='shell'>
    <h1>{html.escape(view_model.chat_tab.title)}</h1>
    <div class='subtitle'>{html.escape(view_model.chat_tab.subtitle)}</div>
    <div class='tabs'>
      <a class='tab {active_chat_class}' href='/?tab=chat'>Chat</a>
      <a class='tab {active_monitor_class}' href='/?tab=monitor'>Monitor</a>
      <a class='tab quick-onboarding' href='/onboarding'>Providers</a>
    </div>
    <div class='panel'>
      {panel_html}
    </div>
  </div>
  <script>
    const chatLog = document.getElementById('chat-log');
    if (chatLog) {{
      chatLog.scrollTop = chatLog.scrollHeight;
    }}
  </script>
</body>
</html>
"""


class StarshipWebHandler(BaseHTTPRequestHandler):
    view_model = None
    onboarding_view_model = None

    def do_GET(self) -> None:  # noqa: N802
        request_path = self.path.split("?", 1)[0]
        self.onboarding_view_model.refresh_readiness()
        if request_path == "/onboarding":
            body = render_onboarding_page(self.onboarding_view_model).encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if request_path != "/":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        if self.onboarding_view_model.should_gate_to_onboarding():
            self.send_response(HTTPStatus.SEE_OTHER)
            self.send_header("Location", "/onboarding")
            self.end_headers()
            return
        if "fresh=1" in self.path:
            self.view_model.runtime.captain_chat_session.reset_conversation()
        if "tab=monitor" in self.path:
            self.view_model.active_tab = "monitor"
        elif "tab=chat" in self.path:
            self.view_model.active_tab = "chat"
        self.view_model.refresh()
        body = render_page(self.view_model).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        content_length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(content_length).decode("utf-8")
        if self.path == "/chat":
            if self.onboarding_view_model.should_gate_to_onboarding():
                self.send_response(HTTPStatus.SEE_OTHER)
                self.send_header("Location", "/onboarding")
                self.end_headers()
                return
            self.view_model.submit_user_message(payload)
            self.send_response(HTTPStatus.SEE_OTHER)
            self.send_header("Location", f"/?tab={self.view_model.active_tab}")
            self.end_headers()
            return
        if self.path == "/onboarding/select":
            self.onboarding_view_model.submit_provider_selection(payload)
            self.send_response(HTTPStatus.SEE_OTHER)
            self.send_header("Location", "/onboarding")
            self.end_headers()
            return
        if self.path == "/onboarding/setup":
            self.onboarding_view_model.submit_provider_setup(payload)
            next_location = "/?tab=chat&fresh=1" if not self.onboarding_view_model.should_gate_to_onboarding() else "/onboarding"
            self.send_response(HTTPStatus.SEE_OTHER)
            self.send_header("Location", next_location)
            self.end_headers()
            return
        if self.path == "/onboarding/reset":
            self.onboarding_view_model.reset_onboarding()
            try:
                self.view_model.runtime.captain_chat_session.reset_conversation()
            except Exception:
                pass
            self.send_response(HTTPStatus.SEE_OTHER)
            self.send_header("Location", "/onboarding")
            self.end_headers()
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return


def launch_web_ui(host: str = "127.0.0.1", port: int = 8765, base_path: Path | None = None) -> None:
    root = (base_path or Path.cwd()).resolve()
    onboarding_view_model = build_onboarding_screen_view_model(root)
    runtime = build_runtime(base_path=root, launch_policy=onboarding_view_model.get_launch_policy())
    StarshipWebHandler.view_model = build_captain_console_screen_view_model(runtime)
    StarshipWebHandler.onboarding_view_model = onboarding_view_model
    server = ThreadingHTTPServer((host, port), StarshipWebHandler)
    print(json.dumps({"status": "online", "url": f"http://{host}:{port}/onboarding", "captain": runtime.starship.captain.name}))
    server.serve_forever()
