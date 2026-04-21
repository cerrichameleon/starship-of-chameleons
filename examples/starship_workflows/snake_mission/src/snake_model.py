from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import random
from typing import Iterable


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class Direction(Enum):
    UP = Point(0, -1)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)

    @property
    def delta(self) -> Point:
        return self.value


OPPOSITE_DIRECTIONS = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}


@dataclass
class SnakeGameState:
    board_width: int
    board_height: int
    snake_segments: list[Point]
    food_position: Point
    current_direction: Direction
    score: int = 0
    is_game_over: bool = False


class SnakeGameModel:
    """Owns the truth of the Snake world so views and test harnesses can read it."""

    def __init__(self, board_width: int = 40, board_height: int = 20, random_seed: int | None = None) -> None:
        self._random = random.Random(random_seed)
        self._board_width = board_width
        self._board_height = board_height
        self._state = self._build_initial_state()

    @property
    def state(self) -> SnakeGameState:
        return self._state

    def _build_initial_state(self) -> SnakeGameState:
        center_x = self._board_width // 2
        center_y = self._board_height // 2
        snake_segments = [
            Point(center_x, center_y),
            Point(center_x - 1, center_y),
            Point(center_x - 2, center_y),
        ]
        food_position = self._spawn_food(excluded_points=snake_segments)
        return SnakeGameState(
            board_width=self._board_width,
            board_height=self._board_height,
            snake_segments=snake_segments,
            food_position=food_position,
            current_direction=Direction.RIGHT,
        )

    def change_direction(self, requested_direction: Direction) -> None:
        if requested_direction == OPPOSITE_DIRECTIONS[self._state.current_direction]:
            return
        self._state.current_direction = requested_direction

    def advance_one_tick(self) -> None:
        if self._state.is_game_over:
            return

        current_head = self._state.snake_segments[0]
        movement = self._state.current_direction.delta
        next_head = Point(current_head.x + movement.x, current_head.y + movement.y)

        if self._collides_with_wall(next_head) or self._collides_with_body(next_head):
            self._state.is_game_over = True
            return

        self._state.snake_segments.insert(0, next_head)

        if next_head == self._state.food_position:
            self._state.score += 1
            self._state.food_position = self._spawn_food(excluded_points=self._state.snake_segments)
        else:
            self._state.snake_segments.pop()

    def snapshot_rows(self) -> list[str]:
        rows: list[str] = []
        for y_position in range(self._state.board_height):
            row_characters: list[str] = []
            for x_position in range(self._state.board_width):
                point = Point(x_position, y_position)
                if x_position in {0, self._state.board_width - 1} or y_position in {0, self._state.board_height - 1}:
                    row_characters.append("#")
                elif point == self._state.food_position:
                    row_characters.append("*")
                elif point == self._state.snake_segments[0]:
                    row_characters.append("@")
                elif point in self._state.snake_segments[1:]:
                    row_characters.append("o")
                else:
                    row_characters.append(" ")
            rows.append("".join(row_characters))
        return rows

    def _spawn_food(self, excluded_points: Iterable[Point]) -> Point:
        excluded_point_set = set(excluded_points)
        while True:
            candidate = Point(
                self._random.randint(1, self._board_width - 2),
                self._random.randint(1, self._board_height - 2),
            )
            if candidate not in excluded_point_set:
                return candidate

    def _collides_with_wall(self, point: Point) -> bool:
        return point.x in {0, self._state.board_width - 1} or point.y in {0, self._state.board_height - 1}

    def _collides_with_body(self, point: Point) -> bool:
        body_without_tail = self._state.snake_segments[:-1]
        return point in body_without_tail
