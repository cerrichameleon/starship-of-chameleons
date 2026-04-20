# Captain Channel Options

## The Problem
During prototyping, the user is still talking to OpenClaw through the existing bot surface.
But the desired long-term model is:
- user talks to Captain
- Captain orchestrates the crew
- OpenClaw acts as substrate rather than the visible personality layer

At the same time, during development, the user still needs a way to speak to the underlying OpenClaw layer for debugging, setup, and architecture work.

## Best Prototype Options

### Option 1, Relay Mode
OpenClaw remains the visible surface.
OpenClaw relays user messages into the Captain layer and relays Captain responses back.

Pros:
- easiest to prototype
- no extra user confusion about separate channels yet
- debug access remains available
- works with current Telegram bot setup

Cons:
- not fully immersive
- boundary between OpenClaw and Captain remains visible

### Option 2, Captain Mode Toggle
Use a mode switch so the same Telegram chat can behave in two modes:
- Build Mode, talking to OpenClaw directly
- Captain Mode, talking to the Captain persona and command layer

This could be exposed with Telegram inline buttons.

Example buttons:
- Talk to Captain
- Talk to OpenClaw
- Mission Status
- Pause Mission

Pros:
- same chat, low friction
- easy transition between debug and immersive use
- preserves a clean mental model

Cons:
- requires explicit mode state tracking
- replies must clearly reflect active mode

### Option 3, Separate Captain Channel
OpenClaw remains one bot or session, Captain gets another dedicated surface.

Pros:
- very clean conceptual separation
- stronger immersion

Cons:
- more setup complexity
- more channel/account management
- worse for fast prototyping

## Recommendation
For the prototype, use **Option 2, Captain Mode Toggle**.

Why:
- it keeps a single Telegram thread
- it allows fast switching between development mode and live mission mode
- it matches the requirement that the user may want to speak directly to OpenClaw during the buildout
- Telegram supports inline buttons, which gives a clean control surface

## Suggested Prototype Behavior

### Build Mode
The user is speaking to OpenClaw directly.
Use this for:
- architecture work
- debugging
- code changes
- protocol design
- emergency override

### Captain Mode
The user is speaking to the Captain.
OpenClaw acts as the transport and substrate.
Use this for:
- mission requests
- status updates
- command decisions
- progress inquiries
- high-level coordination

### Status Buttons
The chat can expose buttons like:
- Enter Captain Mode
- Enter Build Mode
- Status
- Pause Mission
- Resume Mission
- Approvals

## Long-Term Direction
Once the system stabilizes, the Captain can become the primary visible interface while OpenClaw recedes into infrastructure.
Until then, OpenClaw should remain available as the backstage operator and debugging layer.
