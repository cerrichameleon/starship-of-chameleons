# v0.1.0 Captain Chat UI

## What this version is
First runnable milestone for the Starship runtime with:
- Captain chat runtime
- web UI face
- CLI face
- registry
- early Captain console layer

## Run the web UI
From the repository root:

```bash
PYTHONPATH=Versions/v0.1.0-captain-chat-ui python3 Versions/v0.1.0-captain-chat-ui/launch_starship_ui.py --host 127.0.0.1 --port 8765 --base-path /home/node/.openclaw/workspace/git/repositories/starship
```

Then open:
- `http://127.0.0.1:8765`

## Run the CLI
```bash
PYTHONPATH=Versions/v0.1.0-captain-chat-ui python3 Versions/v0.1.0-captain-chat-ui/launch_starship_cli.py --mode cli
```

## Notes
- This is a runnable milestone snapshot, not the final architecture.
- The live runtime still depends on API/auth available in the environment.
- Source of truth remains the main repo and git history.
