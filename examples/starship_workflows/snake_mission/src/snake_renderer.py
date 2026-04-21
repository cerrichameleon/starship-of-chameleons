from __future__ import annotations

import curses

from snake_model import SnakeGameModel


class TerminalSnakeRenderer:
    def __init__(self, window: curses.window) -> None:
        self._window = window

    def render(self, model: SnakeGameModel) -> None:
        rows = model.snapshot_rows()
        for y_position, row_text in enumerate(rows):
            self._window.addstr(y_position, 0, row_text)
        self._window.addstr(len(rows), 0, f"score: {model.state.score}  (arrows or wasd, q to quit)")
        self._window.refresh()

    def render_game_over(self, model: SnakeGameModel) -> None:
        self.render(model)
        self._window.addstr(model.state.board_height // 2, max(1, model.state.board_width // 2 - 5), "game over")
        self._window.addstr(model.state.board_height // 2 + 1, max(1, model.state.board_width // 2 - 10), "press any key to exit")
        self._window.refresh()
