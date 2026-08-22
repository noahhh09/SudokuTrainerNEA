from typing import Any, Tuple

import customtkinter as ctk

from src.analysis import Contradictions
from src.core.BoardState import BoardState
from src.core.Cell import Cell

class SudokuGrid(ctk.CTkFrame):
    def __init__(self, master: Any, boardState: BoardState, width: int = 640, height: int = 640, **kwargs):
        super().__init__(master, width, height, **kwargs)

        self.boardState = boardState
        self.sudokuCells: list[list[SudokuCell]] = []

        for i in range(9):
            row: list[SudokuCell] = []

            for j in range(9):
                cell = SudokuCell(self, boardState.getCell(i, j))
                cell.grid(row=i, column=j, padx=1, pady=1)
                row.append(cell)

            self.sudokuCells.append(row)

        self.refresh()

    def refresh(self):
        for i in range(9):
            for j in range(9):
                self.sudokuCells[i][j].refresh(self.boardState.getCell(i, j))

        contradictions = Contradictions.detectContradictions(self.boardState)
        for contra in contradictions:
            for x, y in contra.cellsInvolved:
                self.sudokuCells[x][y].refresh(contradiction=True)


class SudokuCell(ctk.CTkFrame):
    largeFont = None

    def __init__(self, master: Any, cell: Cell, size=64, **kwargs):
        super().__init__(master, width=size, height=size, border_width=2, border_color="#000000", **kwargs)

        self.cell = cell

        if SudokuCell.largeFont is None:
            SudokuCell.largeFont = ctk.CTkFont(size=20, weight='bold')

        self.pack_propagate(False)

        self.valueLabel = ctk.CTkLabel(self, text=str(cell.getValue() or ""), font=SudokuCell.largeFont)
        self.valueLabel.place(relx=0.5, rely=0.5, anchor="center")

    def refresh(self, cell: Cell | None = None, contradiction: bool = False):
        if cell is not None:
            self.cell = cell

        self.valueLabel.configure(text=str(self.cell.getValue() or ""))

        if self.cell.getValue() is None:
            pass # populate candidates here

        if contradiction:
            self.configure(fg_color="#ff0000")
        else:
            self.configure(fg_color="transparent")