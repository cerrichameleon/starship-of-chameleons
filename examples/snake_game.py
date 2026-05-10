from __future__ import annotations

import curses
import random
from dataclasses import dataclass


BOARD_WIDTH = 40
BOARD_HEIGHT = 20
TICK_MS = 180


@dataclass(frozen=True)
class Point:
    x: int
    y: int


DIRECTIONS = {
    curses.KEY_UP: Point(0, -1),
    curses.KEY_DOWN: Point(0, 1),
    curses.KEY_LEFT: Point(-1, 0),
    curses.KEY_RIGHT: Point(1, 0),
    ord("w"): Point(0, -1),
    ord("s"): Point(0, 1),
    ord("a"): Point(-1, 0),
    ord("d"): Point(1, 0),
}


def spawn_food(snake: list[Point]) -> Point:
    while True:
        food = Point(random.randint(2, BOARD_WIDTH - 3), random.randint(2, BOARD_HEIGHT - 3))
        if food not in snake:
            return food


def draw_border(window: curses.window) -> None:
    for x in range(BOARD_WIDTH):
        window.addch(0, x, "#")
        window.addch(BOARD_HEIGHT - 1, x, "#")
    for y in range(BOARD_HEIGHT):
        window.addch(y, 0, "#")
        window.addch(y, BOARD_WIDTH - 1, "#")


def run_game(window: curses.window) -> None:
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
    window.keypad(True)
    window.nodelay(True)
    window.timeout(TICK_MS)

    snake = [
        Point(BOARD_WIDTH // 2, BOARD_HEIGHT // 2),
        Point(BOARD_WIDTH // 2 - 1, BOARD_HEIGHT // 2),
        Point(BOARD_WIDTH // 2 - 2, BOARD_HEIGHT // 2),
    ]
    direction = Point(1, 0)
    food = spawn_food(snake)
    score = 0

    while True:
        draw_border(window)
        window.addstr(BOARD_HEIGHT, 0, f"score: {score}  (arrows or wasd, q to quit)")

        key = window.getch()
        if key == ord("q"):
            break
        if key in DIRECTIONS:
            proposed = DIRECTIONS[key]
            if not (proposed.x == -direction.x and proposed.y == -direction.y):
                direction = proposed

        head = Point(snake[0].x + direction.x, snake[0].y + direction.y)

        body_without_tail = snake[:-1]
        if (
            head.x in {0, BOARD_WIDTH - 1}
            or head.y in {0, BOARD_HEIGHT - 1}
            or head in body_without_tail
        ):
            for index, segment in enumerate(snake):
                window.addch(segment.y, segment.x, "@" if index == 0 else "o")
            window.addch(food.y, food.x, "*")
            window.addstr(BOARD_HEIGHT // 2, BOARD_WIDTH // 2 - 5, "game over")
            window.addstr(BOARD_HEIGHT // 2 + 1, BOARD_WIDTH // 2 - 10, "press any key to exit")
            window.nodelay(False)
            window.getch()
            break

        tail_to_clear = snake[-1] if head != food else None
        snake.insert(0, head)
        if head == food:
            score += 1
            food = spawn_food(snake)
        else:
            removed_tail = snake.pop()
            window.addch(removed_tail.y, removed_tail.x, " ")

        window.addch(food.y, food.x, "*")
        for index, segment in enumerate(snake):
            window.addch(segment.y, segment.x, "@" if index == 0 else "o")
        window.refresh()


if __name__ == "__main__":
    curses.wrapper(run_game)
