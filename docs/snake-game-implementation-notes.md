# Snake Game Implementation Notes

## Work Log
- Chose a terminal Python implementation to maximize simplicity and immediate playability.
- Chose `curses` from the Python standard library for keyboard input and screen drawing.
- Kept the game in a single file because the first delivery goal is tiny scope and immediate reviewability.
- Preserved conceptual separation using helper functions and named data structures instead of splitting into premature modules.

## Role Mapping
- Senior Software Project Manager: defined scope and documentation expectations.
- Scrum Master: kept the process lightweight rather than bureaucratic.
- UI Coder: responsible for rendering, controls, score display, and game-over messaging.
- Backend Coder: responsible for game state, movement, growth, collision rules, and food spawning.

## Design Decisions
- Use a rectangular bordered board.
- Use `@` for snake head, `o` for body, and `*` for food.
- Support both arrow keys and WASD.
- Disallow instant reverse-direction input to avoid self-clip bugs.
- Use fixed tick timing for predictability.
- End on collision rather than wrapping for simpler rules.

## Documentation Doctrine Applied
- Code should remain small and inspectable.
- Functions should have obvious names.
- Comments should be easy to add wherever future ambiguity may appear.
- The point is not only to make the game, but to make the path legible.

## Next Obvious Improvements
- Restart without exiting
- High-score persistence
- Title screen
- Difficulty scaling
- Browser version for easier sharing
