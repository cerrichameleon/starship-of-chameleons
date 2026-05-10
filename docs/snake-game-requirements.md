# Snake Game Requirements and User Stories

## Functional Requirements
1. The game shall start when launched from the command line.
2. The player shall control the snake with arrow keys or WASD.
3. The snake shall move on a steady fixed tick.
4. The snake shall grow when it eats food.
5. The score shall increase when food is eaten.
6. Food shall never spawn on the snake body.
7. The game shall end on wall collision.
8. The game shall end on self-collision.
9. The game shall display a game-over message.
10. The player shall be able to quit with `q`.

## Non-Functional Requirements
1. The game should use only the Python standard library.
2. The implementation should be short, readable, and well-commented.
3. The code should use explicit names and clear structure.
4. The game should be simple to review and maintain.

## User Stories
- As a player, I want to start the game immediately so I can play without setup friction.
- As a player, I want clear controls so I can move confidently.
- As a player, I want visible food and score so I understand my progress.
- As a player, I want the game to end clearly when I crash so the rules feel fair.
- As a reviewer, I want readable code and docs so I can understand how the game was built.
- As a future maintainer, I want comments and clean structure so I can extend the game without guesswork.

## Acceptance Checks
- Launch command works.
- Controls work.
- Food consumption works.
- Growth works.
- Score works.
- Collision detection works.
- Quit works.
- Code review is straightforward.
