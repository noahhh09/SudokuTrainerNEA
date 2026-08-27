from typing import Any

import customtkinter as ctk

from src.analysis import BoardUtils
from src.core.BoardState import BoardState
from src.render.components.SudokuGrid import SudokuGrid
from tests.test_board_state import createRandomBoardState

class SudokuPage(ctk.CTkFrame):
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)

        self.boardState = BoardUtils.copyAndPopulateCandidates(createRandomBoardState(64))
        self.sudokuGrid = SudokuGrid(self, self.boardState)
        self.sudokuGrid.place(relx=0.01, rely=0.499, anchor="w")