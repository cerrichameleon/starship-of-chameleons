# Starship of Chameleons Protocol

The Starship of Chameleons protocol for AI agent management.

An upgrade project for OpenClaw, but architected to outlive any single provider or runtime.

## Status
Bootstrap started locally.

## Runnable X-Wing Slice
A runnable Captain/Uhura prototype now exists.

Concept:
- Captain is the ship brain
- Uhura is the secure comms officer
- Uhura opens only approved channels
- Uhura tells the Captain when a channel is open
- Uhura keeps the channel open until the Captain closes it
- Uhura can diagnose channel state and writes an audit log

Run it:

```bash
cd starship-of-chameleons-protocol
PYTHONPATH=src python3 examples/xwing_demo.py demo
```

Notes:
- The Captain brain uses a provider adapter interface, not OpenClaw-specific core logic.
- Current adapters: `openclaw`, `mock`
- The OpenClaw adapter uses `OPENAI_API_KEY` if present.
- If the key is missing or the API call fails, the demo falls back to an offline Captain reply.
- Uhura audit records are written to `var/uhura_audit.log`.
- Active channel state persists in `var/uhura_state.json`, so the channel can stay open across separate commands until the Captain closes it or TTL expires.

Provider swap example:

```bash
PYTHONPATH=src python3 examples/xwing_demo.py demo --provider mock
```

## Captain chat proof of concept
You can now talk directly to the Captain in a simple local chat loop.

One-shot message:

```bash
PYTHONPATH=src python3 examples/captain_chat.py "Captain, give me a bridge update" --provider mock
```

Interactive mode:

```bash
PYTHONPATH=src python3 examples/captain_chat.py --interactive --provider mock
```

Session status:

```bash
PYTHONPATH=src python3 examples/captain_chat.py --status --provider mock
```

Conversation state is persisted in `var/captain_chat_state.json`.

## Working Idea
This repository holds the code and design for the Starship of Chameleons Protocol, a provider-agnostic orchestration layer built around explicit crew roles, Captain-first interaction, and swappable brains.

## Current Known Facts
- Name: Starship of Chameleons Protocol
- Goal: create a child-simple, Captain-first multi-agent system
- Core law: providers are adapters, never the ship itself
- Full design details live in the white paper and evolving local docs

## Runnable X-Wing Slice
A runnable Captain/Uhura prototype now exists.

Concept:
- Captain is the ship brain-facing command role
- Uhura is the secure comms officer
- Uhura opens only approved channels
- Uhura tells the Captain when a channel is open
- Uhura keeps the channel open until the Captain closes it
- Uhura can diagnose channel state and writes an audit log

Run it:

```bash
cd starship-of-chameleons-protocol
PYTHONPATH=src python3 examples/xwing_demo.py demo
```

Notes:
- The Captain brain uses a provider adapter interface, not OpenClaw-specific core logic.
- Current adapters: `openclaw`, `mock`
- The OpenClaw adapter uses `OPENAI_API_KEY` if present.
- If the key is missing or the API call fails, the demo falls back to an offline Captain reply.
- Uhura audit records are written to `var/uhura_audit.log`.
- Active channel state persists in `var/uhura_state.json`, so the channel can stay open across separate commands until the Captain closes it or TTL expires.

Provider swap example:

```bash
PYTHONPATH=src python3 examples/xwing_demo.py demo --provider mock
```

## Captain chat proof of concept
You can now talk directly to the Captain in a simple local chat loop.

One-shot message:

```bash
PYTHONPATH=src python3 examples/captain_chat.py "Captain, give me a bridge update" --provider mock
```

Interactive mode:

```bash
PYTHONPATH=src python3 examples/captain_chat.py --interactive --provider mock
```

Session status:

```bash
PYTHONPATH=src python3 examples/captain_chat.py --status --provider mock
```

Conversation state is persisted in `var/captain_chat_state.json`.

## Immediate Next Steps
1. connect the Captain chat loop to a live provider-backed Captain by default
2. let Captain delegate to internal Chameleons
3. let Chief Engineer outfit Chameleons with role-appropriate brains
4. add resilience supervision and failure recovery
5. keep changes small and push early/often
