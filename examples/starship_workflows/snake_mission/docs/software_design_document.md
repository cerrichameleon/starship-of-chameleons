# Software Design Document - Snake

## Document Purpose
Describe how the Snake game becomes software. This document is about implementation structure, responsibilities, testability, and delivery approach.

## Software Goal
Implement a tiny, local, playable Snake game with clear code structure and enough separation to support unit testing and future autoplay or harness modes.

## Delivery Context
This mission runs inside the Starship repository as an example workflow. The implementation should be isolated to this example workspace so the crew can use version control without colliding with unrelated protocol work.

## Architectural Approach
Use a layered structure inspired by MVVM-style thinking.

### Proposed Layers
- Model
  - Game state
  - Snake body positions
  - Food position
  - Board dimensions
  - Score
  - Current direction
  - Game-over state
- World/State Wrapper or ViewModel-like layer
  - Exposes safe, structured snapshots of the world
  - Applies translation from game state to renderable or testable state
  - Supports future autoplay/test harness logic
- View
  - Terminal rendering for current delivery
- Controller/Input layer
  - Maps keypresses to game commands

## Module Plan
- `src/snake_model.py`
  - state structures and core game rules
- `src/snake_renderer.py`
  - terminal rendering logic
- `src/snake_controls.py`
  - input mapping and command validation
- `src/snake_game.py`
  - runtime orchestration
- `tests/`
  - unit tests for model behavior

## Key Design Decisions
- Separate core rules from rendering so the game is testable without curses.
- Keep rendering simple and terminal-based for the first delivery.
- Prefer deterministic update logic.
- Prevent direct reverse movement.
- Make food spawning explicit and testable.

## Unit Testing Strategy
Write tests for:
- initial game state
- direction changes
- invalid reverse movement rejection
- food consumption
- snake growth
- score increase
- wall collision
- self-collision

## Version Control Expectations
- Project manager defines tasks before coding starts.
- Each coder should work against isolated files or tightly scoped changes.
- Commits should be small, clear, and attributable.
- Integration should happen through reviewed steps, not blind overwrites.

## Future Extension Notes
- Add autoplay harness mode using direct world-state access
- Add browser rendering layer
- Add replay logging
- Add difficulty scaling
