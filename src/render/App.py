from typing import Tuple

import customtkinter

from src.analysis import BoardUtils
from src.core.BoardState import BoardState
from src.render.SudokuGrid import SudokuGrid
from tests.test_board_state import createRandomBoardState

class App(customtkinter.CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.title("Sudoku Trainer")
        self.geometry("1280x720")

        self.boardState = createRandomBoardState(64)
        self.sudokuGrid = SudokuGrid(self, self.boardState)
        self.sudokuGrid.place(relx=0.01, rely=0.5, anchor="w")
