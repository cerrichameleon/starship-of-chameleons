# Starship Software Design Document

## Overview
The Starship is a Captain-first, provider-agnostic, multi-agent runtime. The user should interact with the Captain while the rest of the crew works below deck through clear command structure, real internal communication, and observable runtime state.

## Requirements
- The Starship must remain provider-agnostic. Providers are interchangeable brain adapters, not the identity of the ship.
- The Starship must be Captain-first. The user talks to the Captain, while other Chameleons operate internally through delegation, collaboration, and reporting.
- The Starship must support dynamic crew design. Crew structure should be proposed from mission needs, approved, then instantiated, rather than hardcoded in advance.
- All agent-bearing roles must be Chameleons with real brains, and the Chief Engineer should be responsible for outfitting and changing those brains.
- The runtime must survive independently of any one face. Terminal, web UI, desktop UI, or chat surfaces should all be interchangeable views over one running ship.
- The architecture must keep one true model. View layers should remain thin and reflect live runtime truth rather than becoming alternate sources of state.
- The Starship must maintain a real operational state machine, with readable manifest output generated from live subsystems such as crew, mission state, dry dock, monitoring, and provider selection.
- Launch should produce a short manifest readout that tells the user how the ship is outfitted right now, including provider path, fallback order, crew count, dry-dock or mission state, and any important warnings.
- The Captain should speak from real runtime/configuration truth, not from hand-written boilerplate.
- Default brain priority must cascade from Codex to OpenAI API to Gemini API, and launch should clearly disclose which path is active and whether token-using paths are in play.
- Mission continuity matters. The Starship should preserve enough logs, directives, artifacts, and mission context to resume meaningful work across restarts.
- The system should support supervised self-work, where the Starship can help build itself under review, with Cerri remaining in the oversight and QA loop.
- A QuickStart installer should let a new user configure providers and launch the Starship with minimal friction, without shell spelunking or repeated setup rituals.

## Design priorities
- Favor readable, well-commented, auditable code over cleverness.
- Preserve meaningful runnable milestones.
- Keep collaboration transparent, observable, and easy to inspect.
- Optimize for local usefulness, morphability, and steady real-world progress over premature scale theater.
