from typing import Any, Tuple

import customtkinter as ctk
import tkinter as tk

from src.analysis import Contradictions
from src.core.BoardState import BoardState
from src.core.Cell import Cell

class SudokuGrid(ctk.CTkFrame):
    def __init__(self, master: Any, boardState: BoardState, width: int = 640, height: int = 640, **kwargs):
        super().__init__(master, width, height, fg_color="black", **kwargs)

        self.boardState = boardState
        self.sudokuCells: list[list[SudokuCell]] = []

        for i in range(9):
            row: list[SudokuCell] = []

            for j in range(9):
                cell = SudokuCell(self, i, j, boardState.getCell(i, j))

                leftpad = 5 if (j % 3 == 0 and j != 0) else 1
                toppad = 5 if (i % 3 == 0 and i != 0) else 1

                cell.grid(row=i, column=j, padx=(leftpad, 1), pady=(toppad, 1))
                row.append(cell)

            self.sudokuCells.append(row)

        self.redraw()

    def redraw(self):
        for i in range(9):
            for j in range(9):
                self.sudokuCells[i][j].redraw(self.boardState.getCell(i, j))

        contradictions = Contradictions.detectContradictions(self.boardState)
        for contra in contradictions:
            for x, y in contra.cellsInvolved:
                self.sudokuCells[x][y].redraw(contradiction=True)


class SudokuCell(ctk.CTkFrame):
    valueFont = None
    candidateFont = None

    def __init__(self, master: Any, row: int, col: int, cell: Cell, size=64, **kwargs):
        super().__init__(master, width=size, height=size, **kwargs)

        self.row = row
        self.col = col
        self.cell = cell
        self.size = size

        if SudokuCell.valueFont is None or SudokuCell.candidateFont is None:
            SudokuCell.valueFont = ctk.CTkFont(size=self.size // 3 + 8, weight='bold')
            SudokuCell.candidateFont = ctk.CTkFont(size=self.size // 8 + 4)

        self.pack_propagate(False)

        self.canvas = tk.Canvas(self, width=self.size, height=self.size)
        self.canvas.pack()

    def redraw(self, cell: Cell | None = None, contradiction: bool = False):
        if cell is not None:
            self.cell = cell

        assert SudokuCell.valueFont
        assert SudokuCell.candidateFont

        self.canvas.delete("all")

        if self.cell.getValue() is not None:
            self.canvas.create_text(self.size // 2, self.size // 2, text=str(self.cell.getValue()), font=SudokuCell.valueFont, tags="value")
        else:
            for candidate in self.cell.getCandidates():
                row = (candidate - 1) // 3
                col = (candidate - 1) % 3

                self.canvas.create_text((col + 0.5) * (self.size / 3), (row + 0.5) * (self.size / 3), font=SudokuCell.candidateFont, text=candidate, tags="candidate", fill="#444444")

        if contradiction:
            self.canvas.configure(bg="#ff0000")
        else:
            self.canvas.configure(bg="white")