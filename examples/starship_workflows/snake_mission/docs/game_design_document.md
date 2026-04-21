# Game Design Document - Snake

## Document Purpose
Describe the game as a player-facing designed experience. This is the crew's living definition of what the game is.

## Game Summary
Snake is a small arcade game in which the player steers a growing snake around a bounded field, collecting food while avoiding collisions.

## Design Goals
- Very easy to learn
- Immediately playable
- Clean rules
- Fast feedback loop
- Suitable as a first Starship game mission

## Target Player
A human reviewer who wants a tiny game that works immediately and is easy to understand.

## Core Gameplay Loop
1. Player starts the game.
2. Snake moves continuously.
3. Player changes direction to avoid collision and reach food.
4. Food increases score and snake length.
5. Difficulty gradually increases through survival pressure.
6. Collision ends the run.

## Game Rules
- The snake moves one grid step per tick.
- The snake may move up, down, left, or right.
- The snake may not reverse directly into itself.
- Eating food increases the score by one.
- Eating food grows the snake by one segment.
- Hitting a wall ends the game.
- Hitting the snake's own body ends the game.

## Scoring
- +1 per food consumed
- Final score shown on game over

## Visual Elements
- Border wall
- Snake head
- Snake body
- Food marker
- Score line
- Game over message

## Controls
- Arrow keys
- WASD keys
- Q to quit

## UX Notes
- The game should visibly persist on screen without excessive flicker.
- The movement speed should be playable by an average human.
- The player should always be able to distinguish snake, food, and walls.

## Out of Scope for First Delivery
- Sound
- Menus
- Difficulty selection
- Persistent high scores
- Mobile build
- Art pipeline
