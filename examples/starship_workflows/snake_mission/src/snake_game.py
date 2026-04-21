from __future__ import annotations

import curses

from snake_controls import translate_input_to_direction
from snake_model import SnakeGameModel
from snake_renderer import TerminalSnakeRenderer


TICK_MS = 180
CURSES_KEY_NAMES = {
    curses.KEY_UP: "UP",
    curses.KEY_DOWN: "DOWN",
    curses.KEY_LEFT: "LEFT",
    curses.KEY_RIGHT: "RIGHT",
}


def run_game(window: curses.window) -> None:
    curses.noecho()
    curses.cbreak()
    try:
        curses.curs_set(0)
    except curses.error:
        pass

    window.keypad(True)
    window.nodelay(True)
    window.timeout(TICK_MS)

    model = SnakeGameModel()
    renderer = TerminalSnakeRenderer(window)

    while True:
        key_code = window.getch()
        if key_code == ord("q"):
            break

        key_name = CURSES_KEY_NAMES.get(key_code, chr(key_code) if 0 <= key_code <= 255 else "")
        requested_direction = translate_input_to_direction(key_name)
        if requested_direction is not None:
            model.change_direction(requested_direction)

        model.advance_one_tick()
        renderer.render(model)

        if model.state.is_game_over:
            window.nodelay(False)
            renderer.render_game_over(model)
            window.getch()
            break


if __name__ == "__main__":
    curses.wrapper(run_game)
