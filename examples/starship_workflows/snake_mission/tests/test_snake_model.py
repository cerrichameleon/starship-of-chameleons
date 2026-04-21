from __future__ import annotations

from snake_model import Direction, Point, SnakeGameModel


def test_initial_state_has_three_segment_snake() -> None:
    model = SnakeGameModel(board_width=12, board_height=12, random_seed=7)

    assert len(model.state.snake_segments) == 3
    assert model.state.current_direction == Direction.RIGHT
    assert model.state.score == 0
    assert not model.state.is_game_over


def test_reverse_direction_is_ignored() -> None:
    model = SnakeGameModel(board_width=12, board_height=12, random_seed=7)

    model.change_direction(Direction.LEFT)

    assert model.state.current_direction == Direction.RIGHT


def test_food_consumption_increases_score_and_length() -> None:
    model = SnakeGameModel(board_width=12, board_height=12, random_seed=7)
    head = model.state.snake_segments[0]
    model.state.food_position = Point(head.x + 1, head.y)

    model.advance_one_tick()

    assert model.state.score == 1
    assert len(model.state.snake_segments) == 4


def test_wall_collision_ends_the_game() -> None:
    model = SnakeGameModel(board_width=6, board_height=6, random_seed=7)

    model.advance_one_tick()
    model.advance_one_tick()

    assert model.state.is_game_over


def test_self_collision_ends_the_game() -> None:
    model = SnakeGameModel(board_width=8, board_height=8, random_seed=7)
    model.state.snake_segments = [
        Point(4, 4),
        Point(4, 5),
        Point(3, 5),
        Point(3, 4),
    ]
    model.state.current_direction = Direction.LEFT

    model.change_direction(Direction.DOWN)
    model.advance_one_tick()
    model.change_direction(Direction.RIGHT)
    model.advance_one_tick()
    model.change_direction(Direction.UP)
    model.advance_one_tick()

    assert model.state.is_game_over
