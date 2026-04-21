from __future__ import annotations

from snake_model import Direction


KEY_TO_DIRECTION = {
    "UP": Direction.UP,
    "DOWN": Direction.DOWN,
    "LEFT": Direction.LEFT,
    "RIGHT": Direction.RIGHT,
    "w": Direction.UP,
    "s": Direction.DOWN,
    "a": Direction.LEFT,
    "d": Direction.RIGHT,
}


def translate_input_to_direction(key_name: str) -> Direction | None:
    return KEY_TO_DIRECTION.get(key_name)
