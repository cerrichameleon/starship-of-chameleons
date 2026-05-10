# Snake Game Design Document

## Project
Tiny playable Snake game for the Starship game studio proof of concept.

## Purpose
Create a very small, fully playable game that demonstrates the Starship crew can organize, document, and deliver a software artifact through recognizable human-style software practices.

## Product Goal
Deliver a local game that ultra can launch in the morning, play immediately, and inspect alongside the supporting documentation trail.

## Design Principles
- Keep scope intentionally tiny.
- Prefer clarity over cleverness.
- Use standard human software practices so the work is legible and reviewable.
- Document decisions as they are made.
- Favor zero-dependency delivery when possible.

## Player Experience Goal
The player launches the game, quickly understands the controls, moves the snake, eats food, grows, tracks score, and receives a clear game-over state on collision.

## Chosen Delivery Form
- Local Python terminal game
- No external dependencies beyond Python standard library
- Keyboard control using arrow keys or WASD

## Core Features
- Start immediately on launch
- Move snake on a fixed tick
- Eat food to grow
- Track score
- End game on wall collision or self-collision
- Allow quit via keyboard

## Constraints
- Must be simple enough to complete quickly
- Must be playable on the local machine without extra installation steps
- Must be readable for review by a human overseer
- Must use clear code structure and comments

## Crew Interpretation
- Senior Software Project Manager: define scope and review structure
- Scrum Master: keep execution lightweight and coordinated
- UI Coder: player-facing display and input behavior
- Backend Coder: game loop, rules, collision, score, food spawning

## Architecture Direction
A single-file implementation is acceptable for this tiny first game, provided responsibilities remain easy to understand.

Logical separation should still be visible through function boundaries:
- input handling
- movement and game update
- rendering
- food spawning
- game-over handling

## Risks
- Overengineering such a tiny game
- Poor terminal compatibility
- Input handling bugs
- Reverse-direction bug
- Food spawning on the snake body

## Success Criteria
- Game launches with `python3 examples/snake_game.py`
- Game is playable with keyboard input
- Score increases correctly
- Snake grows correctly
- Collisions end the game correctly
- Human reviewer can understand how the implementation works quickly
