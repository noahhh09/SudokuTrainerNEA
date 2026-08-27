from typing import Any

import customtkinter as ctk

from src.analysis import BoardUtils
from src.render.components.SudokuGrid import SudokuGrid
from tests.test_board_state import createRandomBoardState

class SudokuPage(ctk.CTkFrame):
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)

        self.boardState = BoardUtils.copyAndPopulateCandidates(createRandomBoardState(64))
        self.sudokuGrid = SudokuGrid(self, self.boardState)
        self.sudokuGrid.place(relx=0.01, rely=0.1, anchor="nw")

        self.buttons = []
        self.buttonsContainer = ctk.CTkFrame(self)
        for i in range(1, 10):
            button = ctk.CTkButton(self.buttonsContainer, width=32, height=32,  text=str(i), command=lambda i=i: self.updateSelectedCellValue(i))
            button.grid(row=0, column=i - 1)
            self.buttons.append(button)

        self.undoButton = ctk.CTkButton(self.buttonsContainer, width=32, height=32, text=" ", command=lambda: self.updateSelectedCellValue(None))
        self.undoButton.grid(row=0, column=len(self.buttons))
        self.buttons.append(self.undoButton)

        self.buttonsContainer.place(relx=0.01, rely=0.99, anchor="sw")


        self.master.bind("<BackSpace>", lambda _: self.updateSelectedCellValue(None))
        self.master.bind("<KeyRelease>", lambda e: self.handleKeyPress(e))

    def updateSelectedCellValue(self, n: int | None):
        row, col = self.sudokuGrid.selectedCellPosition
        if row is not None and col is not None:
            self.boardState.getCell(row, col).setValue(n)
            self.sudokuGrid.redrawCell(row, col)

    def handleKeyPress(self, event):
        if event.char in "123456789" and len(event.char) == 1: 
            try:
                value = int(event.char)
                self.updateSelectedCellValue(value)
            except ValueError as e:
                pass