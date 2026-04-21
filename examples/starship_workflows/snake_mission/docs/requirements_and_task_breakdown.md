# Requirements and Task Breakdown

## Functional Requirements
1. The game must launch locally with Python.
2. The game must display a bounded board.
3. The game must render the snake, food, and score.
4. The player must control the snake with arrow keys or WASD.
5. The snake must move on a fixed tick.
6. Food consumption must grow the snake and increment score.
7. Wall collision must end the game.
8. Self-collision must end the game.
9. The game must be organized so core logic can be unit tested.

## Non-Functional Requirements
1. Use clear names and comments.
2. Keep the first delivery small and reviewable.
3. Avoid external dependencies.
4. Preserve a clear document trail.
5. Use version control to isolate work.

## User Stories
- As a player, I want immediate playability so I can test the game quickly.
- As a reviewer, I want the design documented so I can inspect the thinking.
- As a developer, I want the logic separated from the terminal layer so I can unit test it.
- As a project manager, I want tasks split cleanly so multiple coders do not collide.

## Task Breakdown
### Software Project Manager
- Finalize GDD and SDD
- Derive requirements and user stories
- Divide work into coder assignments
- Review integration status

### Coder One
- Implement model/state logic
- Implement collision and score behavior
- Add unit tests for core rules

### Coder Two
- Implement rendering and controls
- Implement runtime orchestration
- Assist with integration fixes

## Suggested Commit Boundaries
1. Commit docs and task breakdown
2. Commit snake model and tests
3. Commit renderer and controls
4. Commit runtime integration
5. Commit mission log and review notes
