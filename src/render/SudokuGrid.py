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
    largeFont = None
    candidateFont = None

    def __init__(self, master: Any, cell: Cell, size=64, **kwargs):
        super().__init__(master, width=size, height=size, border_width=2, border_color="#000000", corner_radius=0, **kwargs)

        self.cell = cell

        if SudokuCell.largeFont is None or SudokuCell.candidateFont is None:
            SudokuCell.largeFont = ctk.CTkFont(size=20, weight='bold')
            SudokuCell.candidateFont = ctk.CTkFont(size=10)

        self.pack_propagate(False)
        self.grid_propagate(False)

        self.valueLabel = ctk.CTkLabel(self, text=str(cell.getValue() or ""), font=SudokuCell.largeFont)

        self.candidateLabels: list[ctk.CTkLabel] = []
        for i in range(0, 9):
            label = ctk.CTkLabel(self, text=str(i+1), font=SudokuCell.candidateFont, fg_color="transparent", text_color="#aaaaaa", width=0, height=0)
            self.candidateLabels.append(label)

        for i in range(3):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)

        self.valueLabel.lift()

    def redraw(self, cell: Cell | None = None, contradiction: bool = False):
        if cell is not None:
            self.cell = cell

        if self.cell.getValue() is not None:
            for label in self.candidateLabels:
                label.grid_forget()

            self.valueLabel.configure(text=str(self.cell.getValue() or ""))
            self.valueLabel.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.valueLabel.place_forget()

            candidates = self.cell.getCandidates()

            for i, label in enumerate(self.candidateLabels):
                if i + 1 in candidates:
                    label.grid(row=(i // 3), column=(i % 3), padx=2, pady=2, sticky="nsew")
                else:
                    label.grid_forget()


        if contradiction:
            self.configure(fg_color="#ff0000")
        else:
            self.configure(fg_color="transparent")