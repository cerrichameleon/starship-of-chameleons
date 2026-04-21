from __future__ import annotations

from snake_model import Direction, Point, SnakeGameModel


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_initial_state_has_three_segment_snake() -> None:
    model = SnakeGameModel(board_width=12, board_height=12, random_seed=7)

    assert_true(len(model.state.snake_segments) == 3, "expected three snake segments at startup")
    assert_true(model.state.current_direction == Direction.RIGHT, "expected initial direction to be right")
    assert_true(model.state.score == 0, "expected initial score of zero")
    assert_true(not model.state.is_game_over, "game should not start in game-over state")


def test_reverse_direction_is_ignored() -> None:
    model = SnakeGameModel(board_width=12, board_height=12, random_seed=7)
    model.change_direction(Direction.LEFT)
    assert_true(model.state.current_direction == Direction.RIGHT, "reverse direction should be ignored")


def test_food_consumption_increases_score_and_length() -> None:
    model = SnakeGameModel(board_width=12, board_height=12, random_seed=7)
    head = model.state.snake_segments[0]
    model.state.food_position = Point(head.x + 1, head.y)
    model.advance_one_tick()

    assert_true(model.state.score == 1, "score should increment after eating food")
    assert_true(len(model.state.snake_segments) == 4, "snake should grow after eating food")


def test_wall_collision_ends_the_game() -> None:
    model = SnakeGameModel(board_width=6, board_height=6, random_seed=7)
    model.advance_one_tick()
    model.advance_one_tick()
    assert_true(model.state.is_game_over, "wall collision should end the game")


def test_self_collision_ends_the_game() -> None:
    model = SnakeGameModel(board_width=8, board_height=8, random_seed=7)
    model.state.snake_segments = [Point(4, 4), Point(4, 5), Point(3, 5), Point(3, 4)]
    model.state.current_direction = Direction.LEFT
    model.change_direction(Direction.DOWN)
    model.advance_one_tick()
    model.change_direction(Direction.RIGHT)
    model.advance_one_tick()
    model.change_direction(Direction.UP)
    model.advance_one_tick()
    assert_true(model.state.is_game_over, "self-collision should end the game")


def main() -> None:
    tests = [
        test_initial_state_has_three_segment_snake,
        test_reverse_direction_is_ignored,
        test_food_consumption_increases_score_and_length,
        test_wall_collision_ends_the_game,
        test_self_collision_ends_the_game,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS all {len(tests)} snake model tests")


if __name__ == "__main__":
    main()
