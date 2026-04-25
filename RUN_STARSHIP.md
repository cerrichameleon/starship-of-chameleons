# Run Starship

## Simplest launcher from the repo root

```bash
./starship
```

This launches the web UI to the onboarding flow first at `/onboarding`, not straight into raw Captain chat.

## Install a global alias once

```bash
./install_starship_alias.sh
```

Then you can launch from anywhere with:

```bash
starship
```

## Install or refresh `engage`

```bash
./install_engage_alias.sh
```

That creates or updates:

```bash
/usr/local/bin/engage
```

so `engage` points at the moved Starship launcher in this repo and opens onboarding first.

If you have an older host-side `engage` script, check that it points at:

```bash
/home/node/.openclaw/workspace/git/repositories/starship
```

or your equivalent host checkout path, not the old pre-move repo location.

## What the launcher does
- checks for a real Captain brain using the onboarding-selected provider order when one exists, otherwise falls back to the default order: Codex OAuth, then OpenAI API, then Gemini API
- chooses an available localhost port automatically
- starts the Starship web UI
- routes `/` into onboarding until you explicitly choose provider paths and complete enough setup to unlock the Captain console
- lets you choose provider order before setup, including drag-and-drop reordering in the onboarding screen
- carries that selected provider order into actual Captain launch choice when more than one ready provider exists
- lets you stop after the first successful provider hookup or continue through the rest of the selected providers
- lets you reset onboarding and start over cleanly when you want to re-test first-run behavior
- opens a fresh Captain chat after onboarding so legacy bridge chatter does not leak into the first conversation
- keeps a Providers path available even after launch so you can quickly switch or review brain hookups
- prints the chosen root URL and explicit onboarding URL
- attempts to open the browser directly to onboarding automatically

## Quick way to enter the Starship repo inside Docker

If you still need the container shell for any reason:

```bash
./enter_starship.sh
```

## Requirements
- Python 3 available on the host
- either a Codex OAuth profile, `OPENAI_API_KEY`, or `GEMINI_API_KEY`/`GOOGLE_API_KEY` available for real-brain launch
- project checked out locally

## Current goal
The launcher should be one command, obvious, and repeatable. No manual path-juggling should be required.
